""" 아직 미완성 """
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import datetime

st = datetime.datetime.now().timestamp()
es = Elasticsearch(["13.125.246.197", "52.79.215.253", "52.79.250.228"],
                   http_auth=('elastic', 'rkwjs12#'),
                   port=9200)
index_name = "iot-daeyoung-ha-831"
print(es.info())

body = {
    "_source": ['message'],
    "query": {
        "match_all": {}
    },
    "sort": ["_doc"]
}

scroller = scan(client=es, query=body, index=index_name)


