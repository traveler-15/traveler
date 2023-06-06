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
        print(result['items'])
        result2 = [{'title': '몽탄', 'link': 'http://www.mongtan.co.kr','address': '서울특별시 용산구 한강로1가 251-1', 'mapx': '33.3590628', 'mapy': '126.534361'},
                  {'title': '포석로 소<b>갈비</b>찜', 'link': 'https://www.instagram.com/poseok_ro', 'category': '음식점>한식', 'description': '', 'telephone': '', 'address': '경상북도 경주시 황남동 228-1', 'roadAddress': '경상북도 경주시 포석로1068번길 22', 'mapx': '35.1795543', 'mapy': '129.0756416'},
                  {'title': '우목정', 'link': 'http://blog.naver.com/kim5325167', 'category': '한식>육류,고기요리', 'description': '', 'telephone': '', 'address': '경기도 포천시 이동면 장암리 283', 'roadAddress': '경기도 포천시 이동 면 화동로 1974', 'mapx': '344792', 'mapy': '602563'},
                  {'title': '소옥', 'link': 'http://instagram.com/so.ok_official', 'category': '음식점>한식', 'description': '', 'telephone': '', 'address': '경상북도 경주시 황남동 224-7 1층', 'roadAddress': '경상북도 경주시 포석로1050번길 29 1층', 'mapx': '509737', 'mapy': '360086'},
                  {'title': '원조이동김미자할머니<b>갈비</b>  포천이동본점', 'link': 'http://www.김미자할머니갈비.kr/', 'category': '한식>육류,고기요리', 'description': '', 'telephone': '', 'address': '경기도 포천시 이동면 장암리 216-3', 'roadAddress': '경기도 포천시 이동면 화동로 2087', 'mapx': '344545', 'mapy': '603667'}
                  ]
        return jsonify(result['items'])
    else: #성공시 'result':'실패'
        return jsonify({'result': "실패"})

if __name__ == '__main__':
   app.run('0.0.0.0', port=3000, debug=True)