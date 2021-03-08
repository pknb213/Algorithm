import motor.motor_asyncio
import asyncio

class Gmarket():
    def __init__(self):
        host = "localhost"
        port = 27017
        self.url = "https://m.gmarket.co.kr/n/superdeal?categoryCode=400000{}&categoryLevel=1"
        # self.category_id = [135,136,137,139,140,143,146,148,149,151,152] #174
        self.category_id = [135,136] #174
        self.client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    async def main():
        return await asyncio.gather(*[session(GMARKET_URL.format(str(i))) for i in CATEGORY_ID])

    async def session(_url):
        with requests.Session() as s:
            req = s.post(_url)
            html_tree = html.fromstring(req.content)

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
            return [{"title": title[i], "price": price[i], "url": url_info[i],
                     "img": base64.b64encode(urlopen("http:" + img[i]).read())} for i in range(len(title))]

class Gsshop():
    def __init__(self):
        host = "localhost"
        port = 27017
        self.url = "https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378{}"
        self.category_id = [773,781,794,813,825,783]
        self.client = motor.motor_asyncio.AsyncIOMotorClient(host, port)


