from flask import Flask
from ddb import DDB
from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch

load_dotenv()

app = Flask(__name__)


es = Elasticsearch('[엘라스틱_서버_IP_주소]:9200')

# 일반적인 라우트 방식입니다.
@app.route('/api/article/<category>')
def board(category):
    return "그냥 보드"

# URL 에 매개변수를 받아 진행하는 방식입니다.
@app.route('/api/article/<article_id>')
def board_view(article_id):
    return article_id

# 위에 있는것이 Endpoint 역활을 해줍니다.
@app.route('/boards',defaults={'page':'index'})
@app.route('/boards/<page>')
def boards(page):
    return page+"페이지입니다."

app.run(host="localhost",port=5001,debug=True)