from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import client
from datetime import datetime, timedelta
import pprint
import time

"""
200의 Loop 결과
>> END : 441501105 431598514 1:32:09.440749
제거 된 데이터의 수 : 9,902,591
제거 되지 못한 데이터 수 : 97,409
원인 : 모름
증상 : if 남은데이터 == 0: break 조건이 일치하지 않아 무한 루프 됨.
방안 : 30초 동안 처리하지 못할 경우 다시 반복문 continue 처리.
"""


pp = pprint.PrettyPrinter(indent=4)
es = Elasticsearch(["13.125.246.197", "52.79.215.253", "52.79.250.228"],
                   http_auth=('elastic', 'rkwjs12#'),
                   port=9200)
es.info()
st = datetime.now()
body = {
    "query": {
        "match_all": {}
    },
    "sort": ["_doc"]
}
s = es.count(index='iot-skmagic')['count']
for i in range(0, 200):
    es = Elasticsearch(["13.125.246.197", "52.79.215.253", "52.79.250.228"],
                       http_auth=('elastic', 'rkwjs12#'),
                       port=9200)
    scroller = helpers.scan(client=es, query=body, index='iot-skmagic')
    at = datetime.now()
    a = es.count(index='iot-skmagic')['count']
    print("Before :", a)
    c = 1
    NUMBER_OF_DELETION = 50000
    id_list = []
    body2 = {
        'query': {
            'terms': {
                "_id": id_list
            }
        }
    }
    for sc in scroller:
        if c >= NUMBER_OF_DELETION:
            break
        elif c % (NUMBER_OF_DELETION/2) == 0:
            print(c, " Search ~", datetime.now() - st)
        # pp.pprint(sc)
        # es.delete(index='iot-skmagic', id=sc['_id'])
        id_list.append(sc['_id'])
        c += 1
    # time.sleep(10)
    # while len(id_list) != NUMBER_OF_DELETION-1
    res = es.delete_by_query(index='iot-skmagic', body=body2, wait_for_completion=False)
    print("Time : ", datetime.now(), datetime.now() - at, "Delete Count : ", c)
    client.indices.IndicesClient.refresh(self=es,index='iot-skmagic')
    while 1:
        try:
            time.sleep(1)
            res = es.count(index="iot-skmagic")['count']
            if NUMBER_OF_DELETION-1-(a-res) == 0 or datetime.now() - at > timedelta(seconds=30):
                break
        except Exception as e:
            print(e)
    print(">> After : ", i, a, res, NUMBER_OF_DELETION-1-(a-res))
print(">> END :", s, res, datetime.now() - st)