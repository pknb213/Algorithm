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
from Shop_Class import *

INIT_PAGE = 1
# CATEGORY_ID = [135,136,137,139,140,143,146,148,149,151,152]
CATEGORY_ID = [135,136]
GMARKET_URL = "https://m.gmarket.co.kr/n/superdeal?categoryCode=400000{}&categoryLevel=1"


async def main():
    return await asyncio.gather(*[session(GMARKET_URL.format(str(i))) for i in CATEGORY_ID])


async def session(_url):
    with requests.Session() as s:
        req = s.post(_url)
        html_tree = html.fromstring(req.content)

        img = html_tree.xpath('//*[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img/@data-src')
        price = html_tree.xpath('//*[@class="component"]/div/div/div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong/text()')
        price = [v for v in price if v != " "]
        title = html_tree.xpath('//*[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img/@alt')
        url_info = html_tree.xpath('//*[@class="box__itemcard-superdeal--img"]/a/@href')
        # for i in price:
        #     print(">", i, len(price)/3)
        # for i in img:
        #     print(">>", base64.b64encode(urlopen("http:"+i).read()), type(i), len(img))
        # for i in title:
        #     print(">>>", i, len(title))
        # for i in url_info:
        #     print(">>>>", i, len(url_info))
        return [{"title": title[i], "price": price[i], "url": url_info[i], "img": base64.b64encode(urlopen("http:"+img[i]).read())} for i in range(len(title))]


if __name__ == '__main__':
    st = timer()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(main())
    loop.close()
    print(a[0][0], len(a), len(a[0]), len(a[0][0]))
    print(type(a[0]), type(a[0][0]))
    print("실행 시간", timedelta(seconds=timer() - st))


