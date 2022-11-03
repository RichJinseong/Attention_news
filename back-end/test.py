from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()
host = os.environ.get('host')
user = os.environ.get('user')
password = os.environ.get('password')
es = Elasticsearch(host, http_auth=(user, password))

index = "product_list"

doc = {
          "category": "skirt",
          "c_key": "1234",
          "price": '11.400',
          "status": 2,
          "date": "2021-07-08"
}

body = {
    "query" :{
    "match_all":{}
}
}
res = es.search(index='test_list', body=body)
print(111, res)