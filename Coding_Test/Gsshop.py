import motor.motor_asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Gsshop():
    def __init__(self):
        host = "localhost"
        port = 27017
        self.url = "https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378{}"
        self.category_id = [773,781,794,813,825,783]
        self.client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    async def extract_data(self, i):
        try:
            el_img = i.find_element_by_xpath('a[@class="prd-item"]/div[@class="prd-img"]/img')
            el_title = i.find_element_by_xpath('a[@class="prd-item"]/dl[@class="prd-info"]/dt[@class="prd-name"]')
            el_price = i.find_element_by_xpath('a[@class="prd-item"]/dl[@class="prd-info"]/dd[@class="price-info"]/span/span/strong')
            el_url = i.find_element_by_xpath('a[@class="prd-item"]')
            # await asyncio.sleep(0.1)
            await self.client["shop_db"]["gsshop"].insert_one({
                "title": el_title.text.strip(),
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
            for i in range(1, 4):
                driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                                          options=options)
                driver.implicitly_wait(2)
                driver.get(url)
                if i != 1:
                    driver.get(url+"#0_popular_{}".format(str(i)))
                    driver.refresh()
                    # next_page = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pageNavigation']/*[@class='paging']/a[7]")))
                    # next_page.click()
                elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="prd-list type-4items"]/ul/li')))
                # print(url, len(elements))
                res = await asyncio.gather(*[self.extract_data(i) for i in elements])
                driver.close()
            return res
        except Exception as e:
            print("Error >>", url, e)

    async def main(self):
        return await asyncio.gather(*[self.get_elements(self.url.format(str(i))) for i in self.category_id])

