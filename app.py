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
    query_receive = request.form['query_give']#넘겨받은 여행지
    client_id = "mvz_k56LApeEKijNqLM7"
    client_secret = "oTc3GwSvzo"

    encText = urllib.parse.quote(query_receive)
    url = "https://openapi.naver.com/v1/search/local.json?query=" + encText + \
                "&display=10"#받을 데이터 갯수

    request1 = urllib.request.Request(url)
    request1.add_header("X-Naver-Client-Id",client_id)
    request1.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request1)
    rescode = response.getcode()
    if(rescode==200):#성공시 'result':데이터
        response_body = response.read()
        result = json.loads(response_body)
        return jsonify({'result': result})
    else:#성공시 'result':'실패'
        return jsonify({'result': "실패"})


if __name__ == '__main__':
   app.run('0.0.0.0', port=3000, debug=True)