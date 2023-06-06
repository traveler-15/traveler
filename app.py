from flask import Flask, render_template, jsonify, request
import urllib.request
import json
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.lrw9rvw.mongodb.net/?retryWrites=true&w=majority')
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
        # result를 배열 안에 객체 형태로 제작 부탁드립니다.
        result = json.loads(response_body)

        WGS84 = {'proj':'latlong', 'datum':'WGS84', 'ellps':'WGS84',}
        KATEC = {'proj':'tmerc', 'lat_0':'38N', 'lon_0':'128E', 'ellps':'bessel',
        'x_0':'400000', 'y_0':'600000', 'k':'0.9999', 'a':'6377397.155', 'b':'6356078.9628181886',
        'towgs84':'-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43', 'units':'m'}

        inProj = Proj(**KATEC)
        outProj = Proj(**WGS84)

        x2, y2 = transform(inProj, outProj, 309947, 552092)
        print(x2, y2)

        return jsonify(result['items'])
    else: #성공시 'result':'실패'
        return jsonify({'result': "실패"})

if __name__ == '__main__':
   app.run('0.0.0.0', port=3000, debug=True)