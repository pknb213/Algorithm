"""#############################################################################################
2020_07_09 Python-Elasticsearch API Code By Cheon YoungJo v.7.0.4
Basic APIs
    - bulk( body , index = None , doc_type = None , params = None , headers = None )
    : 단일 요청으로 여러 추가 / 수정 / 삭제 작업을 할 수 있습니다.
    - count( body = None , index = None , params = None , headers = None )
    : 쿼리와 일치하는 문서 수를 반환.
    - create( index , id , body , doc_type = None , params = None , headers = None )
    : index에 새 문서를 작성한다. 동일한 ID가 존재하면 409 응답을 한다.
    - delete( index , id , doc_type = None , params = None , headers = None )
    : index에서 문서를 제거합니다.
    - delete_by_query( index , body , params = None , headers = None )
    : 쿼리와 일치하는 문서를 제거.
    - exists( index , id , params = None , headers = None )
    : 문서가 index에 있는지 여부를 리턴합니다.
    - explain( index , id , body = None , params = None , headers = None )
    : 특정 쿼리와 일치하는 이유에 대해 정보를 반환.
    - get( index , id , params = None , headers = None )
    : 문서를 리턴합니다.
    - index( index , body , id = None , params = None , headers = None )
    : index에 문서를 작성하거나 수정합니다.
    - info( params = None , 헤더 = None )
    : 클러스테에 대한 기본 정보를 반환합니다.
    - mget( body , index = None , params = None , headers = None )
    : 한 번의 요청으로 여러 문서를 가져옵니다.
    - msearch( body , index = None , params = None , headers = None )
    : 한 번의 요청으로 여러 검색 작업을 실행합니다.
    - reindex( body , params = None , headers = None )
    : 하나의 index에서 다른 index로 문서를 복사하거나, 선택적으로 쿼리를 통해
    소스 문서를 필터링하거나, 대상 index설정을 변경하거나 원격 클러스터에서 문서를 가져올 수 있다.
    - scroll( body = None , scroll_id = None , params = None , headers = None )
    : 단일 검색 요청에서 많은 수의 결과를 검색할 수 있습니다.
    - search( body = None , index = None , params = None , headers = None )
    : 쿼리와 일치하는 결과를 반환합니다.
    - search_shards( index = None , params = None , headers = None )
    : 검색 요청이 실행될 index 및 shard에 대한 정보를 반환합니다.
    - update( index , id , body , doc_type = None , params = None , headers = None )
    : 스크립트 또는 문서를 업데이트 합니다.
    - update_by_query( index , body = None , params = None , headers = None )
    : 소스를 변경하지 않고 index의 모든 문서에 대해 업데이트를 수행합니다.
Helper APIs (Basic API를 추상화하는 도우미 함수)
    : Basic apis와 iterable을 사용합니다. actions(반복 가능하며 모든 iterable이 생성자가 될 수 있음)
    대량의 경우 데이터를 메모리에 로드하지 않고도 indexing을 할 수 있기 때문에 대부분의 경우 이상적.
    - elasticsearch.helpers.streaming_bulk( client , actions , chunk_size = 500
    , max_chunk_bytes = 104857600 , raise_on_error = TRUE , expand_action_callback = <function  expand_action>
    , raise_on_exception = TRUE는 , MAX_RETRIES는 = 0 , = 2 initial_backoff , max_backoff = 600 , yield_ok = TRUE
    , * args , ** kwargs)
    : 전달된 iterable에서 action을 소비하고 각각의 action 마다 결과를 생성합니다.
    - elasticsearch.helpers.parallel_bulk( client , actions , thread_count = 4 , chunk_size = 500
    , max_chunk_bytes = 104857600 , queue_size = 4 , expand_action_callback = <function expand_action>
    , * args , ** kwargs )
    : 한 번에 여러 스레드에서 실행됩니다.
    - elasticsearch.helpers.bulk( client , actions , stats_only = False , * args , ** kwargs )
    : Basic bulk보다 친화적인 인터페이스를 제공하는 helper api이며 chunk 단위로 elasticsearch에 전송.
    - elasticsearch.helpers.scan( client , query = None , scroll = '5m' , raise_on_error = True
    , preserve_order = False , size = 1000 , request_timeout = None , clear_scroll = True , scroll_kwargs = None
    , ** kwargs )
    : Basic scan요청에 모두 hits된 결과를 생성하는 단순한 iterator입니다.
    - elasticsearch.helpers.reindex( client , source_index , target_index , query = None , target_client = None
    , chunk_size = 500 , scroll = '5m' , scan_kwargs = {} , bulk_kwargs = {} )
    : 주어진 쿼리를 만족하는 하나의 index에서 다른 cluster로 모든 문서를 다시 적재합니다. 쿼리가 없으면 모든 문서를
    재 적재합니다. helper는 주로 호환성과 더 유연하기 때문에 사용하는게 적합합니다.
Asyncio APIs (python3.6이상 elsaticsearch-py v.7.8이상 지원)
    : ASGI(Asynchronous Server Gateway Interface)는 비동기 I/O를 사용하여 더 나은 성능을 달성하는
    python web application program을 제공하는 새로운 방법. ASGI framework 예로는 FastAPI, Django 3.0
    및 Starlette가 있습니다. (APIs 생략 https://elasticsearch-py.readthedocs.io/en/master/async.html)
#############################################################################################"""
from elasticsearch import Elasticsearch

es = Elasticsearch(["13.125.246.197", "52.79.215.253", "52.79.250.228"],
                   http_auth=('elastic', 'rkwjs12#'),
                   port=9200)
print(es.info())




