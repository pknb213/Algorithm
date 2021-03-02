import motor.motor_asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Gmarket():
    def __init__(self):
        host = "localhost"
        port = 27017
        self.url = "https://m.gmarket.co.kr/n/superdeal?categoryCode=400000{}&categoryLevel=1"
        # self.category_id = [135,136,137,139,140,143,146,148,149,151,152] #174
        self.category_id = [135,136] #174
        self.client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    async def extract_data(self, i):
        try:
            el_img = i.find_element_by_xpath(
                'div/div/div[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img')
            el_price = i.find_element_by_xpath(
                'div/div/div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong')
            el_url = i.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a')
            # await asyncio.sleep(0.1)
            await self.client["shop_db"]["gmarket"].insert_one({
                "title": el_img.get_attribute("alt"),
                "price": el_price.text,
                "img": el_img.screenshot_as_base64,
                "url": el_url.get_property("href")
            })
        except Exception as e:
            print("Error >>", i.text, e)

    async def get_elements(self, url):
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                                      options=options)
            driver.implicitly_wait(2)
            driver.get(url)
            elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="component"]')))
            # elements = driver.find_elements_by_xpath('//*[@class="component"]')
            # print(url, len(elements))
            res = await asyncio.gather(*[self.extract_data(i) for i in elements])
            driver.close()
            return res
        except Exception as e:
            print("Error >>", url, e)

    async def main(self):
        return await asyncio.gather(*[self.get_elements(self.url.format(str(i))) for i in self.category_id])
