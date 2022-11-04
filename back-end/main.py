from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

load_dotenv()
host = os.environ.get('host')
user = os.environ.get('user')
password = os.environ.get('password')
es = Elasticsearch(host, http_auth=(user, password))

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
es_index = 'news'
category_dict = {
    'news': '뉴스',
    'sports': '스포츠',
    'life': '생활',
    'money': '경제',
    'tech': '기술',
    'travel': '여행',
    'opinion': '기타'
}

ko_category_dict = {
    '뉴스':'news',
    '스포츠':'sports',
    '생활': 'life',
    '경제':'money',
    '기술':'tech',
    '여행':'travel',
    '기타':'opinion',
}


@app.route('/api/articles/<category>')
def article_view(category):
    news_list = []
    body = {
        "size": 100,  # max get value count
        "sort": [
            {"date": {"order": "asc"}},
        ],
        "query": {
            "match": {
                "category": ko_category_dict[category]
            }
        }
    }
    res = es.search(index=es_index, body=body)
    article_list = res['hits']['hits']
    for i in article_list:
        try:
            news_format = {
                'article_id': i['_source']['uid'],
                'date': i['_source']['date'],
                'platform': i['_source']['platform'],
                'en_category': i['_source']['category'].split(',')[0],
                'en_headline': i['_source']['en_headline'],
                'ko_category': category_dict[i['_source']['category'].split(',')[0]],
                'ko_headline': i['_source']['ko_headline'],
            }
            news_list.append(news_format)
        except Exception as e:
            print('에러', e)
    return jsonify({'data': news_list})


@app.route('/api/article/<article_id>')
def article_detail(article_id):
    body = {
        "size": 100,  # max get value count
        "query": {
            "match": {
                "uid": article_id
            }
        }
    }
    res = es.search(index=es_index, body=body)
    article_list = res['hits']['hits']
    print(res)
    i = article_list[0]
    article = {
        'article_id': i['_source']['uid'],
        'date': i['_source']['date'],
        'platform': i['_source']['platform'],
        'en_category': i['_source']['category'].split(',')[0],
        'en_headline': i['_source']['en_headline'],
        'ko_category': category_dict[i['_source']['category'].split(',')[0]],
        'ko_headline': i['_source']['ko_headline'],
        'en_content': i['_source']['en_content'],
        'en_summarization': i['_source']['en_summarization'],
        'ko_content': i['_source']['ko_content'],
        'ko_summarization': i['_source']['ko_summarization'],
        'link': 'https://www.usatoday.com/story/news/politics/2022/11/03/pelosi-released-hospital-hammer-attack-depape/8261279001/'
    }

    return jsonify({'data': article})


if os.environ.get('prod'):
    app.run(host="3.36.247.224", port=8080, debug=True)
else:
    app.run(host="localhost", port=5001, debug=True)