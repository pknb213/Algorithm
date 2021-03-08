import requests
import asyncio
import pprint
import base64
import sys
from lxml import html
from multiprocessing import cpu_count
from bs4 import BeautifulSoup
from timeit import default_timer as timer
from datetime import timedelta
from urllib.request import urlopen
sys.path.append("./")
from Shop_Class import Gmarket, Gsshop

INIT_PAGE = 1
# CATEGORY_ID = [135,136,137,139,140,143,146,148,149,151,152]
CATEGORY_ID = [135,136]
GMARKET_URL = "https://m.gmarket.co.kr/n/superdeal?categoryCode=400000{}&categoryLevel=1"


if __name__ == '__main__':
    st = timer()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    # Todo : Class Object 선언
    gmarket = Gmarket()
    gsshop = Gsshop()
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(gmarket.main())
    # b = loop.run_until_complete(gsshop.main())
    loop.close()
    print(a[0][0], len(a), len(a[0]), len(a[0][0]))
    print(type(a[0]), type(a[0][0]))
    # print(b[0][0], len(b), len(b[0]), len(b[0][0]))
    # print(type(b[0]), type(b[0][0]))
    res = []
    [res.extend(a[i]) for i in range(len(a))]
    print("Count :", len(res))
    print("실행 시간", timedelta(seconds=timer() - st))
    # Todo : Mongo Insert


