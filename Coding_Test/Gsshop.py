import motor.motor_asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import asyncio


class Gsshop():
    def __init__(self):
        host = "localhost"
        port = 27017
        self.url = "https://www.gsshop.com/shop/sect/sectL.gs?sectid=13787{}#0_popular_1"
        self.category_id = [73, 81, 88, 94]
        self.client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    async def sub2(self, i):
        try:
            el_img = i.find_element_by_xpath('a[@class="prd-item"]/div[@class="prd-img"]/img/')
            el_title = i.find_element_by_xpath('a[@class="prd-item"]/div[@class="prd-info"]/dt[@class="prd-name"]')
            el_price = i.find_element_by_xpath('a[@class="prd-item"]/div[@class="prd-info"]/dd[@class="price-info"]')
            el_url = i.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a')
            # await asyncio.sleep(0.1)
            await self.client["test"]["test"].insert_one({
                "title": el_img.get_attribute("alt"),
                "price": el_price.text,
                "img": el_img.screenshot_as_base64,
                "url": el_url.get_property("href")
            })
        except Exception as e:
            pass

    async def sub(self, url):
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                                      options=options)
            driver.implicitly_wait(2)
            driver.get(url)
            elements = driver.find_elements_by_xpath('//*[@class="prd-list type-4items"]/ul/li')
            print(url, len(elements))
            res = await asyncio.gather(*[self.sub2(i) for i in elements])
            driver.close()
            return res
        except Exception as e:
            print("Error >>", url, e)

    async def main(self, url):
        return await asyncio.gather(*[self.sub(url.format(str(i))) for i in self.category_id])