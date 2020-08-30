from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from operator import itemgetter
from ast import literal_eval
import time, datetime, pprint, json
import pandas as pd


def add_error_type(_dict):
    device_arr = ['22822', '22862', '22844', '22856', '22711', '22871', '22680', '22713', '22639', '22860', '22867',
                  '22874', '22881', '22876', '22671', '22854', '22846', '22821']
    if 'error_type' in _dict:
        pass
    elif _dict['deviceId'] in device_arr:
        if _dict['deviceId'] == '22822':
            if "20200302181700" <= _dict['reqTime'] < "20200302214700":
                _dict['error_type'] = '1'
                return _dict
            elif "20200307000000" <= _dict['reqTime'] < "20200528000000":
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22862' and "20200416000000" <= _dict['reqTime'] < "20200528000000":
            _dict['error_type'] = '1'
            return _dict
        elif _dict['deviceId'] == '22844':
            if "20200301000000" <= _dict['reqTime'] < "20200302000000":
                _dict['error_type'] = '1'
                return _dict
            elif "20191218000000" <= _dict['reqTime'] < "20200227000000" or \
                    "20200314000000" <= _dict['reqTime'] < "20200528000000":
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22856' and "20200314000000" <= _dict['reqTime'] < "20200528000000":
            _dict['error_type'] = '2'
            return _dict
        elif _dict['deviceId'] == '22711':
            if "20191125000000" <= _dict['reqTime'] < "20191127000000":
                _dict['error_type'] = '1'
                return _dict
            elif "20191212000000" <= _dict['reqTime'] < "20200528000000":
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22871' and "20200501000000" <= _dict['reqTime'] < "20200528000000":
            _dict['error_type'] = '2'
            return _dict
        elif _dict['deviceId'] == '22680' and "20190928000000" <= _dict['reqTime'] < "20200528000000":
            _dict['error_type'] = '1'
            return _dict
        elif _dict['deviceId'] == '22713':
            if "20191028000000" <= _dict['reqTime'] < "20191031000000" or \
                    "20200322000000" <= _dict['reqTime'] < "20200528000000":
                _dict['error_type'] = '1'
                return _dict
            elif "20191028000000" <= _dict['reqTime'] < "20191031000000":
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22639':
            if "20200109203900" <= _dict['reqTime'] < "202001092118" or \
                    "20200127170500" <= _dict['reqTime'] < "20200127201200":
                _dict['error_type'] = '1'
                return _dict
            elif "20190928000000" <= _dict['reqTime'] < "20200528000000":
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22860':
            if "20200412183600" <= _dict['reqTime'] < "20200412190800":
                _dict['error_type'] = '1'
                return _dict
            elif "20200408000000" <= _dict['reqTime'] < "20200415000000":
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22867' and "20200424000000" <= _dict['reqTime'] < "20200428000000":
            _dict['error_type'] = '1'
            return _dict
        elif _dict['deviceId'] == '22874':
            if "20200521134700" <= _dict['reqTime'] < "20200521140800":
                _dict['error_type'] = '1'
                return _dict
            elif "20200430000000" <= _dict['reqTime'] < "20200528000000":
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22881':
            if "20200515122600" <= _dict['reqTime'] < "20200515133000" or \
                    '20200516141700' <= _dict['reqTime'] < '20200516152700' or \
                    '20200519210100' <= _dict['reqTime'] < '20200519222100':
                _dict['error_type'] = '1'
                return _dict
            elif '20200513000000' <= _dict['reqTime'] < '20200528000000':
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22876':
            if "20200516194500" <= _dict['reqTime'] < "20200516204500" or \
                    '20200518192600' <= _dict['reqTime'] < '20200518194600' or \
                    '20200523191000' <= _dict['reqTime'] < '20200523193800':
                _dict['error_type'] = '1'
                return _dict
            elif '20200514000000' <= _dict['reqTime'] < '20200528000000':
                _dict['error_type'] = '2'
                return _dict
            else:
                _dict['error_type'] = '0'
                return _dict
        elif _dict['deviceId'] == '22671' and "20190928000000" <= _dict['reqTime'] < "20200528000000":
            _dict['error_type'] = '1'
            return _dict
        elif _dict['deviceId'] == '22854' and "20200203000000" <= _dict['reqTime'] < "20200210000000":
            _dict['error_type'] = '2'
            return _dict
        elif _dict['deviceId'] == '22846' and "20200102073700" <= _dict['reqTime'] < "20200102081800":
            _dict['error_type'] = '1'
            return _dict
        elif _dict['deviceId'] == '22821' and "20191212000000" <= _dict['reqTime'] < "20191216000000":
            _dict['error_type'] = '2'
            return _dict
        else:
            _dict['error_type'] = '0'
            return _dict
    else:
        _dict['error_type'] = '0'
        return _dict


st = datetime.datetime.now().timestamp()
_KEEP_ALIVE_LIMIT = '1s'
body = {
    "_source": ['message'],
    "query": {
        "match_all": {}
    },
    "sort": ["_doc"]
}

es = Elasticsearch(["13.125.246.197:9200", "52.79.215.253:9200", "52.79.250.228:9200"])
index_name = "iot-daeyoung-ha-831"
# index_name = 'iot-grib-g100sr'
print(es.info())

scroller = scan(client=es, query=body, index=index_name)
# df = pd.DataFrame(scroller)
# df2 = df['_source'].apply(pd.Series)['message'].str.split('|')
# print(df2)

# df = pd.DataFrame(scroller)['_source'].apply(pd.Series)['message'].str.split('|')
# df.to_csv("C:\\Users\\CheonYoungJo\\Desktop\\IotDataSetTest.csv", sep=',', index=None)
# # df = pd.DataFrame(scroller)
# print(df)

count = 0
doc = 1
final_arr = []
for each_result in scroller:
    each_result = each_result['_source']['message'].split('|')
    result_dict = {}
    for i in each_result:
        res = i.split('=')
        """ 실행 시간이 늘어나고 deviceId 같은 예외가 존재 함 """
        # if res[1] == "null":
        #     res[1] = None
        # elif res[1].isdecimal():
        #     res[1] = int(res[1])
        result_dict[res[0]] = res[1]

    """  """
    final_arr.append(add_error_type(result_dict))
    # print(result_dict, len(result_dict), type(result_dict), count)

    """ Generator Limit """
    # if count == 1000000:
    #     break
    if count == 0:
        pass
    elif count % 1000000 == 0:
        """ 100만 건당 4분 정도의 시간 소요되고 CSV 파일 생성까지 30초 정도 걸림 """
        print("[%d] Processing Time : %sm %ss" % (count, int(str(int(datetime.datetime.now().timestamp() - st))) // 60,
                                                  int(str(int(datetime.datetime.now().timestamp() - st))) % 60))
        final_arr = sorted(final_arr, key=itemgetter('reqTime'), reverse=True)
        df = pd.DataFrame(final_arr).to_csv("C:\\Users\\CheonYoungJo\\Desktop\\2020_06_29_DataSet_%d.csv" % doc,
                                            sep=",", index=None)
        final_arr.clear()
        doc += 1

    count += 1

print("[%d] Processing Finish : %sm %ss " % (count, int(str(int(datetime.datetime.now().timestamp() - st))) // 60,
                                             int(str(int(datetime.datetime.now().timestamp() - st))) % 60))
print(final_arr[-1], type(final_arr[-1]))
final_arr = sorted(final_arr, key=itemgetter('reqTime'), reverse=True)
df = pd.DataFrame(final_arr).to_csv("C:\\Users\\CheonYoungJo\\Desktop\\2020_06_29_DataSet_%d.csv" % doc,
                                    sep=",", index=None)
# for i in final_arr:
#     print(i)

# st2 = datetime.datetime.now().timestamp()
# df = pd.DataFrame(final_arr).to_csv("C:\\Users\\CheonYoungJo\\Desktop\\2020_06_29_DataSet.csv", sep=",", index=None)
# print("[%d] DataFrame Making Time : %sm %ss" % (len(final_arr),
#                                                 int(str(int(datetime.datetime.now().timestamp() - st2))) // 60,
#                                                 int(str(int(datetime.datetime.now().timestamp() - st2))) % 60))

# """ 필드 추출 후 1행 만들기 """
# fields_str = next(scroller)['_source']['message'].split('|')
# print(fields_str, type(fields_str))
# fields = []
# values = []
# for i in fields_str:
#     res = i.split('=')
#     fields.append(res[0])
#     values.append(res[1])
#
# print(fields, values, len(fields), len(values))
#
# df = pd.DataFrame(columns=fields)
# df.loc[0] = values
#
# print(df.keys())
#
#
# count = 0
#
# df['message'] = df['_source'].str.split('|')
# df2 = df['_source'].apply(pd.Series).apply(json.loads)
#
# print(df2)


# print(scroller)
# for i in scroller:
#     print(i['_source']['message'])
# df = pd.DataFrame(i['_source']['message'].split('|'))
# print(df)

# # with open("C:\\Users\\CheonYoungJo\\Desktop\\test.csv", "a") as f:
# #     for i in nums:
# #         f.write(str(i) + "\n")


################## Shard 관련
# # Get Number of shards
# shards_info = es.search_shards(index_name)
# num_of_shard = len(shards_info['shards'])
# print("Shard Info : ", shards_info, num_of_shard)
#
# # Shard number to routing key
# shards = {}
# routing = 0
# i = 0
# while len(shards.keys()) < num_of_shard:
#     result = es.search_shards(index_name, routing=i)
#     shard_number = result['shards'][0][0]['shard']
#     if shard_number not in shards:
#         shards[shard_number] = i
#     i += 1
# print(shards)

print("실행 시간 : ", int(str(int(datetime.datetime.now().timestamp() - st))) // 60, "m",
      int(str(int(datetime.datetime.now().timestamp() - st))) % 60, 's')

########################### Scrool ###############
# res = es.search(
#     index=index_name,
#     scroll=_KEEP_ALIVE_LIMIT,
#     size=10000,
#     body=body
# )
# print('Total Doc : ', len(res['hits']['hits']))
#
# sid = res['_scroll_id']
# fetched = len(res['hits']['hits'])
#
# nums = []
# for i in range(fetched):
#     nums.append(res['hits']['hits'][i]['_source'])
#
# t1 = datetime.datetime.now().timestamp()
# while fetched > 0:
#     response = es.scroll(scroll_id=sid, scroll='1s')
#     fetched = len(response['hits']['hits'])
#     print('scroll() Query Length : ', fetched, " [Time: ", datetime.datetime.now().timestamp() - t1, "]")
#     for i in range(fetched):
#         nums.append(response['hits']['hits'][i]['_source'])
#
#
# df = pd.DataFrame(nums[100]['message'].split('|')).to_csv("C:\\Users\\CheonYoungJo\\Desktop\\test.csv", sep='|', index=None)
# print(df)
#
# # with open("C:\\Users\\CheonYoungJo\\Desktop\\test.csv", "a") as f:
# #     for i in nums:
# #         f.write(str(i) + "\n")
#
# pp = pprint.PrettyPrinter(indent=4)
# # pp.pprint(nums)
# print(nums[100]['message'].split('|'), len(nums))
#
