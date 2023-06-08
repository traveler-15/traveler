from flask import Flask, render_template, jsonify, request, redirect, url_for
import urllib.request
import json
from pyproj import Proj, transform

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.lrw9rvw.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'TRAVELER'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms="HS256")
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("member_login_form", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("member_login_form", msg="로그인 정보가 존재하지 않습니다."))
    
    

@app.route("/place/search", methods=["POST"])
def place_search():
    query_receive = request.form['query_give'] #넘겨받은 여행지
    client_id = "mvz_k56LApeEKijNqLM7"
    client_secret = "oTc3GwSvzo"

    encText = urllib.parse.quote(query_receive)
    url = "https://openapi.naver.com/v1/search/local.json?query=" + encText + \
                "&display=5" #받을 데이터 갯수

    request1 = urllib.request.Request(url)
    request1.add_header("X-Naver-Client-Id",client_id)
    request1.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request1)
    rescode = response.getcode()
    if(rescode==200): #성공시 'result':데이터
        response_body = response.read()
        result = json.loads(response_body)
        
        for item in result['items']:
            
            WGS84 = {'proj':'latlong', 'datum':'WGS84', 'ellps':'WGS84',}
            KATEC = {'proj':'tmerc', 'lat_0':'38N', 'lon_0':'128E', 'ellps':'bessel',
            'x_0':'400000', 'y_0':'600000', 'k':'0.9999', 'a':'6377397.155', 'b':'6356078.9628181886',
            'towgs84':'-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43', 'units':'m'}

            inProj = Proj(**KATEC)
            outProj = Proj(**WGS84)

            item['mapy'], item['mapx'] = transform(inProj, outProj, item['mapx'], item['mapy'])
        
        return jsonify(result['items'])
    else: # 성공시 'result':'실패'
        return jsonify({'result': "실패"})

# 찜 데이터 삭제
@app.route('/place/delete', methods=["POST"])
def delete_map():
    token_receive = request.cookies.get('mytoken')
    title_receive = str(request.form['title_give'])
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms="HS256")
        user_id = payload['id']
        db.maps.delete_one({'title':title_receive,'user_id':user_id})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("member_login_form", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("member_login_form", msg="로그인 정보가 존재하지 않습니다."))
    
    
    return jsonify({'msg': "삭제완료!"})


# MongoDB에 데이터 보내기
@app.route("/place/save", methods=["POST"])
def save_map():

    title_receive = request.form['title_give']
    link_receive = request.form['link_give']
    address_receive = request.form['address_give']
    mapx_receive = request.form['mapx_give']
    mapy_receive = request.form['mapy_give']

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms="HS256")
        user_id = db.user.find_one({"id": payload['id']})['id']
    except jwt.ExpiredSignatureError:
        return redirect(url_for("member_login_form", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("member_login_form", msg="로그인 정보가 존재하지 않습니다."))
    
    doc = {
        'title':title_receive,
        'link':link_receive,
        'address':address_receive,
        'mapx':mapx_receive,
        'mapy':mapy_receive,
        'user_id':user_id
    }
    db.maps.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route("/place/show", methods=['GET'])
def show_place():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms="HS256")
        user_id = db.user.find_one({"id": payload['id']})['id']
    except jwt.ExpiredSignatureError:
        return redirect(url_for("member_login_form", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("member_login_form", msg="로그인 정보가 존재하지 않습니다."))
    
    all_maps = list(db.maps.find({"user_id" : user_id},{'_id':False}))
    return jsonify({'result':all_maps})

#####################################################
#회원 가입 API
#####################################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.

@app.route('/register')#회원가입 폼페이지로 이동
def member_save_form():
   return render_template('register.html')

@app.route("/api/register", methods=["POST"])#로그인 폼 페이지로부터 정보를 받아 db member에 저장(중복 방지에 대해 미구현)
def member_save():
    id_receive = request.form['id_give']
    if db.user.find_one({"id": payload['id']})['id'] is None:
        pw_receive = request.form['pw_give']
        nickname_receive = request.form['nickname_give']

        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

        db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

        return jsonify({'result': 'success'})
    else :
        return jsonify({'result': 'ID Duplicated'})
    

#################################
##  로그인을 위한 API            ##
#################################

@app.route('/login')#로그인 폼페이지로 이동
def member_login_form():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route("/api/login", methods=["POST"])
def member_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=3000, debug=True)
   
