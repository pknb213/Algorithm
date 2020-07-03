from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time, datetime

es = Elasticsearch(["52.79.236.72:9200", "52.79.136.180:9200", "15.164.170.224:9200"])
es.info()

index_name = "iot-daeyoung*"

qry1 = {
    "bool": {
        "must": {
            'match_all': {}
        },
        'filter': {
            'range': {
                "reqTime": {
                    "gte": "20200302181700",
                    "lte": "20200302214700"
                }
            }
        }
    },
}

qry = {
    'match_all': {}
}

# ---------------------------------------------
def make_index(es, index_name):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    print(es.indices.create(index=index_name))


new_index = "python_test"
make_index(es, new_index)
# ----------------------------------------------
_str = 0

result = es.search(index=index_name, size=10000, body={'from': 0, 'query': qry}, scroll='1m')
# print(result)
sid = result['_scroll_id']
_len = len(result['hits']['hits'])
print(_len, sid)

r = []
k = 0
p = 1


def add_field(j, _arr):
    hits_arr = _arr['hits']['hits']
    device_id = hits_arr[j]['_source']["deviceId"]
    req_time = hits_arr[i]['_source']["reqTime"]
    device_arr = ['22822', '22862', '22844', '22856', '22711', '22871', '22680', '22713', '22639', '22860', '22867', '22874', '22881', '22876', '22671', '22854', '22846', '22821']

    # print(hits_arr[j]['_source']["message"][-12:-2])
    if hits_arr[j]['_source']["message"][-12:-2] == "error_type":
        pass
    elif device_id in device_arr:
        if device_id == '22822':
            if "20200302181700" <= req_time < "20200302214700":
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif "20200307000000" <= req_time < "20200528000000":
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22862' and "20200416000000" <= req_time < "20200528000000":
            hits_arr[j]['_source']["message"] += "|error_type=1"
        elif device_id == '22844':
            if "20200301000000" <= req_time < "20200302000000":
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif "20191218000000" <= req_time < "20200227000000" or "20200314000000" <= req_time < "20200528000000":
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22856' and "20200314000000" <= req_time < "20200528000000":
            hits_arr[j]['_source']["message"] += "|error_type=2"
        elif device_id == '22711':
            if "20191125000000" <= req_time < "20191127000000":
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif "20191212000000" <= req_time < "20200528000000":
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22871' and "20200501000000" <= req_time < "20200528000000":
            hits_arr[j]['_source']["message"] += "|error_type=2"
        elif device_id == '22680' and "20190928000000" <= req_time < "20200528000000":
            hits_arr[j]['_source']["message"] += "|error_type=1"
        elif device_id == '22713':
            if "20191028000000" <= req_time < "20191031000000" or "20200322000000" <= req_time < "20200528000000":
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif "20191028000000" <= req_time < "20191031000000":
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22639':
            if "20200109203900" <= req_time < "202001092118" or "20200127170500" <= req_time < "20200127201200":
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif "20190928000000" <= req_time < "20200528000000":
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22860':
            if "20200412183600" <= req_time < "20200412190800":
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif "20200408000000" <= req_time < "20200415000000":
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22867' and "20200424000000" <= req_time < "20200428000000":
            hits_arr[j]['_source']["message"] += "|error_type=1"
        elif device_id == '22874':
            if "20200521134700" <= req_time < "20200521140800":
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif "20200430000000" <= req_time < "20200528000000":
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22881':
            if "20200515122600" <= req_time < "20200515133000" or '20200516141700' <= req_time < '20200516152700' or '20200519210100' <= req_time < '20200519222100':
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif '20200513000000' <= req_time < '20200528000000':
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22876':
            if "20200516194500" <= req_time < "20200516204500" or '20200518192600' <= req_time < '20200518194600' or '20200523191000' <= req_time < '20200523193800':
                hits_arr[j]['_source']["message"] += "|error_type=1"
            elif '20200514000000' <= req_time < '20200528000000':
                hits_arr[j]['_source']["message"] += "|error_type=2"
            else:
                hits_arr[j]['_source']["message"] += "|error_type=0"
        elif device_id == '22671' and "20190928000000" <= req_time < "20200528000000":
            hits_arr[j]['_source']["message"] += "|error_type=1"
        elif device_id == '22854' and "20200203000000" <= req_time < "20200210000000":
            hits_arr[j]['_source']["message"] += "|error_type=2"
        elif device_id == '22846' and "20200102073700" <= req_time < "20200102081800":
            hits_arr[j]['_source']["message"] += "|error_type=1"
        elif device_id == '22821' and "20191212000000" <= req_time < "20191216000000":
            hits_arr[j]['_source']["message"] += "|error_type=2"
        else:
            hits_arr[j]['_source']["message"] += "|error_type=0"
    else:
        hits_arr[j]['_source']["message"] += "|error_type=0"


st = datetime.datetime.now().timestamp()
for i in range(_len):
    # print(result['hits']['hits'][i])
    #r.append(result['hits']['hits'][i]['_source']['message'])
    with open("C:\\Users\\CheonYoungJo\\Desktop\\testFile_1.csv", "a") as f:
        add_field(i, result)
        f.write(result['hits']['hits'][i]['_source']['message'] + "\n")

while _len > 0:
    res = es.scroll(scroll_id=sid, scroll='1m')
    _len = len(res['hits']['hits'])
    for i in range(_len):
        # print(res['hits']['hits'][i])
        #r.append(result['hits']['hits'][i]['_source']['message'])
        with open("C:\\Users\\CheonYoungJo\\Desktop\\testFile_"+str(p)+".csv", "a") as f:
            add_field(i, result)
            f.write(result['hits']['hits'][i]['_source']['message'] + "\n")
    k += 1
    print("%d번째 Loop ( %.3f초 경과 )" % (k, float(datetime.datetime.now().timestamp() - st)))
    # if k == 10:
    #     _len = 0
    if k % 100 == 0:
        p += 1

print("끄읕")




