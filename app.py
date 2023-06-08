from flask import Flask, render_template, jsonify, request
import urllib.request
import json
from pyproj import Proj, transform

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.ga3pmrv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

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
    title_receive = str(request.form['title_give'])
    db.maps.delete_one({'title':title_receive})
    return jsonify({'msg': "삭제완료!"})


# MongoDB에 데이터 보내기
@app.route("/place/save", methods=["POST"])
def save_map():
    title_receive = request.form['title_give']
    link_receive = request.form['link_give']
    address_receive = request.form['address_give']
    mapx_receive = request.form['mapx_give']
    mapy_receive = request.form['mapy_give']

    doc = {
        'title':title_receive,
        'link':link_receive,
        'address':address_receive,
        'mapx':mapx_receive,
        'mapy':mapy_receive
    }
    db.maps.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route("/place/show", methods=['GET'])
def show_place():
    all_maps = list(db.maps.find({},{'_id':False}))
    return jsonify({'result':all_maps})


# @app.route('/member/signup')#회원가입 폼페이지로 이동
# def member_save_form():
#    return render_template('signup.html')

# @app.route("/member/save", methods=["POST"])#로그인 폼 페이지로부터 정보를 받아 db member에 저장(중복 방지에 대해 미구현)
# def member_save():
#    name = request.form['name']
#    email = request.form['email']
#    password = request.form['password']
#    nickname = request.form['nickname']
#    doc = {'name':name,'email':email, 'password': password, 'nickname':nickname}
#    db.member.insert_one(doc)
#    return render_template('index.html')

# @app.route('/member/login')#로그인 폼페이지로 이동
# def member_login_form():
#    return render_template('login.html')

# @app.route("/member/login", methods=["POST"])#회원가입 폼 페이지로부터 정보를 받아 db member에서 찾기 (아직 회원 유무, 비번 확인에대해 미구현)
# def member_login():
#    email = request.form['email']
#    password = request.form['password']
#    print(type(db.member.find_one({'email':email , 'password' : password})['nickname']))
   
#    return render_template('index.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=3000, debug=True)
   
