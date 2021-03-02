from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from multiprocessing import cpu_count
from timeit import default_timer as timer
from datetime import timedelta
import pprint, json, time
import asyncio
import motor.motor_asyncio
from pymongo import MongoClient
from Algorithm.Coding_Test.Gmarket import Gmarket

# https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378773#0_popular_4
# https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378781
def extract_product():
    st = timer()
    gsshop_url = "https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378773#0_popular_{}"
    url = "https://m.gmarket.co.kr/n/superdeal?categoryCode=400000{}&categoryLevel=1"
    category_id = [135,136,137,139,140,143,146,148,149,151,152,174]
    # category_id = [174, 136]
    print("-->", timedelta(seconds=timer() - st))

    # async def sub2(i):
    #     try:
    #         el_img = i.find_element_by_xpath(
    #             'div/div/div[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img')
    #         el_price = i.find_element_by_xpath(
    #             'div/div/div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong')
    #         el_url = i.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a')
    #         # await asyncio.sleep(0.1)
    #         await client["test"]["test"].insert_one({
    #             "title": el_img.get_attribute("alt"),
    #             "price": el_price.text,
    #             "img": el_img.screenshot_as_base64,
    #             "url": el_url.get_property("href")
    #         })
    #     except Exception as e:
    #         pass
    #
    # async def sub(url):
    #     try:
    #         options = Options()
    #         options.headless = True
    #         driver = webdriver.Chrome(executable_path="./chromedriver.exe",
    #                                   options=options)
    #         driver.implicitly_wait(2)
    #         driver.get(url)
    #         elements = driver.find_elements_by_xpath('//*[@class="component"]')
    #         print(url, len(elements))
    #         res = await asyncio.gather(*[sub2(i) for i in elements])
    #         driver.close()
    #         return res
    #     except Exception as e:
    #         print("Error >>", url, e)
    #
    # async def main(url):
    #     return await asyncio.gather(*[sub(url.format(str(i))) for i in category_id])

    t = timer()
    # host = "localhost"
    # port = 27017
    # client = motor.motor_asyncio.AsyncIOMotorClient(host, port)
    # client2 = MongoClient(host, port)
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(url))
    gmarket = Gmarket()
    loop.run_until_complete(gmarket.main())
    loop.close()
    print("Async -->", timedelta(seconds=timer() - t))


if __name__ == '__main__':
    st = timer()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    print("Total :", extract_product())

    # make_dynamic_xpath()
    print("실행 시간", timedelta(seconds=timer() - st))
