import motor.motor_asyncio
import requests
import asyncio
import base64
from abc import ABCMeta
from lxml import html
from urllib.request import urlopen


class AbstractEcommerce(metaclass=ABCMeta):
    host = "localhost"
    port = 27017
    client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    async def main(self):
        pass

    @classmethod
    async def extract(cls, _url):
        pass


class Gmarket(AbstractEcommerce):
    def __init__(self):
        self.url = "https://m.gmarket.co.kr/n/superdeal?categoryCode=400000{}&categoryLevel=1"
        self.category_id = [135,136,137,139,140,143,146,148,149,151,152, 174]
        # self.category_id = [135,136]

    async def main(self):
        return await asyncio.gather(*[self.extract(self.url.format(str(i))) for i in self.category_id])

    @classmethod
    async def extract(cls, _url):
        with requests.Session() as s:
            try:
                req = s.post(_url)
                html_tree = html.fromstring(req.content)

                img = html_tree.xpath(
                    '//div[@class="box-product"]/span[@class="box-product__img-product"]/img/@data-src')
                img = [v if v[:7] == "//image" else "//lh3.googleusercontent.com/AN8gkA6tFRLbkOs2RBfC8zCY3cHKEb2GD9kVURQJM3pKyNqv-kWP8-iHD1PdryPWfVc=w600-h600" for v in img]
                price = html_tree.xpath(
                    '//div[@class="box__itemcard--price"]/span[@class="text__item--title"]/span/..')
                price = [v for v in price if v != " "]
                title = html_tree.xpath(
                    '//div[@class="box-product"]/span[@class="box-product__img-product"]/img/@alt')
                url_info = html_tree.xpath('//*[@class="box__itemcard-superdeal--img"]/a/@href')
                # for i in price:
                #     print(">", i, len(price))
                # for i in img:
                #     print(">>", i)
                # for i in title:
                #     print(">>>", i, len(title))
                # for i in url_info:
                #     print(">>>>", i, len(url_info))
                print(len(img), len(price), len(title), len(url_info))
                res = [{
                        "title": title[i],
                        "price": price[i].text_content(),
                        "url": url_info[i],
                        "img": base64.b64encode(urlopen("http:" + img[i]).read())
                    } for i in range(len(title))]
            except Exception as e:
                print(">>>>", e, _url)
                res = []
            return res


class Gsshop(AbstractEcommerce):
    def __init__(self):
        self.url = "https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378{}"
        self.category_id = [773,781,794,813,825,783]

    async def main(self):
        return await asyncio.gather(*[self.extract(self.url.format(str(i))) for i in self.category_id])

    @classmethod
    async def extract(cls, _url):
        with requests.Session() as s:
            try:
                req = s.post(_url)
                html_tree = html.fromstring(req.content)
                # Todo : Change the xpath
                img = html_tree.xpath(
                    '//*[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img/@data-src')
                price = html_tree.xpath(
                    '//*[@class="component"]/div/div/div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong/text()')
                price = [v for v in price if v != " "]
                title = html_tree.xpath(
                    '//*[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img/@alt')
                url_info = html_tree.xpath('//*[@class="box__itemcard-superdeal--img"]/a/@href')
                # for i in price:
                #     print(">", i, len(price)/3)
                # for i in img:
                #     print(">>", base64.b64encode(urlopen("http:"+i).read()), type(i), len(img))
                # for i in title:
                #     print(">>>", i, len(title))
                # for i in url_info:
                #     print(">>>>", i, len(url_info))
                print(len(img), len(price), len(title), len(url_info))
                res = [{
                    "title": title[i],
                    "price": price[i],
                    "url": url_info[i],
                    "img": base64.b64encode(urlopen("http:" + img[i]).read())
                } for i in range(len(title))]
            except Exception as e:
                print(">>>>", e, _url)
                res = []
            return res
