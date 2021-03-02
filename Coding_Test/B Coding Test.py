from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer
from datetime import timedelta
import requests, pprint, datetime, json, time
import asyncio

"""
https://m.gmarket.co.kr/
https://www.gsshop.com/index.gs

데이터 수집 요구사항(1)
- 쇼핑사별로 1000개의 상품 데이터를 수집 및 유지 한다.
- 상품 이름, 가격, 대표이미지, 해당 쇼핑사 상품주소를 필수로 수집한다.
- 필수 수집 데이터 외에 쇼핑사별로 달리 제공한는 데이터는 선택적으로 수집한다.
- 수시로 바뀌는 상품 데이터의 동기화 이슈를 고려해야 한다.
- 대량의 데이터 수집을 짧은 시간안에 처리 하기 위한 시스템 구조를 갖는다.

수집 프로세스 운영 요구사항(2)
- 정해진 xpath로 데이터를 수집하게 되면 추후에 쇼핑 사이트가 변경될 때 마다 변경된
것을 확인 하고, 변경된 사이트에 맞춰서 코드를 수정해야 하기 때문에 유지 보수 비용이
추가로 발생한다.
- 따라서, 고정된 xpath 를 사용하는 것이 아니라 상품의 URL과, 상품명, 가격, 이미지
정보를 입력으로 받으면 동적으로 xpath 정보를 추출하고, 추출된 xpath를 이용해서
데이터를 수집해야 한다.

데이터베이스 구축 요구사항(3)
- 원본(raw) 데이터로 관리되기 위한 최적화된 데이터베이스 구조를 목표로 한다.
- 상품 데이터 모델과 수집 프로세스 운영에 관한 정보를 담는 모델을 고려해야 한다.
- 향후 활용을 위해 데이터 조회에 특화된 스키마 설계가 포함되어야 한다.

선택 요구사항
- 데이터 수집단계에서 프로세스를 추적하고 관리 할 수 있는 툴을 활용한다. 일정 주기마다
배치 처리작업을 수행하고, 수행된 프로세스들에 대한 모니터링이 가능해야 한다.
"""
# Todo : MongoDB 사용, 테이블로 관계형 스키마 사용 ex) 쇼핑몰ID - Product

"""
https://m.gmarket.co.kr/
# 메인화면 후 카테고리 -> 변경 필요
https://m.gmarket.co.kr/n/superdeal
https://m.gmarket.co.kr/n/superdeal?categoryCode=400000174&categoryLevel=1
url : //div[@class="box__itemcard-superdeal--inner"]//div[@class="box__itemcard-superdeal--img"]//*[@class="box__itemcard-superdeal--link"]
img : //*[@class="box-product__img-product"]/img'
title : //*[@class="text__title"]
price : //*[@class="text__price"] 

https://www.gsshop.com/index.gs
# 영상/음향 가전 페이지 1 ~ 60
https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378798&lseq=414301-10&gsid=gnb-AU414301-AU414301-10
https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378798&lseq=414301-10&gsid=gnb-AU414301-AU414301-10#0_popular_2 ... 60
url : //section[@class="prd-list type-4items"]/ul/li/a[@class="prd-item"] href
img : //section[@class="prd-list type-4items"]/ul/li/a[@class="prd-item"]/div[@class="prd-img"]/img src
title : //section[@class="prd-list type-4items"]/ul/li/a[@class="prd-item"]/div[@class="prd-name"]/dl/dt/span
price : //section[@class="prd-list type-4items"]/ul/li/a[@class="prd-item"]/div[@class="price-info"]/span[@class="price"]/span[@class="set-price"]/strong 
"""
# Todo : 큰 Div를 가져오고 하위 태그 루프 돌리면서 가져오게 하는게 효율이 좋을거 같은데
# Todo : //div[text() = "일치하는 Text"]     //div[contains(text(), "포함하는 Text")]


def convert_image_to_binary():
    # image to Binary Test
    import cv2, base64
    cv = cv2.imread("./test.png")
    bcv = cv2.imencode('.PNG', cv)[1].tobytes()
    print(bcv, type(bcv))

    with open('test.png', "rb") as f:
        print("\n", base64.b64encode(f.read()), type(base64.b64encode(f.read())))

    with open('test.png', "rb") as f:
        print("\n", bytearray(f.read())[0], type(bytearray(f.read())[0]))


def make_dynamic_xpath():
    """
    :param: URL, Title, Price, Img
    :return: Xpath as Json
    """
    # Todo : Please In to the Try Exception
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                              options=options)
    driver.implicitly_wait(2)
    url = 'http://www.gsshop.com/prd/prd.gs?prdid=37216130'
    title = '[애플망고]딥브이원피스'
    price = '8,900'
    img = 'http://image.gsshop.com/image/37/21/37216130_L1.jpg'
    url = 'https://m.gmarket.co.kr/n/superdeal'
    title = '[쇼케이스]G마켓 단독 신발/의류+사은품 '
    price = '39,000'
    img = '//image.gmarket.co.kr/hanbando/202102/573640b1-e25f-4c73-8221-4b1aa82260ba.jpg'
    driver.get(url)

    import itertools
    import re

    def xpath_soup(element):
        """
        Generate xpath of soup element
        :param element: bs4 text or node
        :return: xpath as string
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:  # parent: bs4.element.Tag
            previous = itertools.islice(parent.children, 0, parent.contents.index(child))
            xpath_tag = child.name
            xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
            components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    raw_html = driver.page_source
    soup = BeautifulSoup(raw_html, 'lxml')
    img_xpath = xpath_soup(soup.find(attrs={'src': img}))
    title_xpath = xpath_soup(soup.find(text=title))
    price_xpath = xpath_soup(soup.find(text=price))  # re.complie(price) OK But [] No
    driver.quit()
    xpath_json = {
        'title': title_xpath,
        'price': price_xpath,
        'img': img_xpath
    }
    print(xpath_json)

    # Todo : Expected Result
    json_data = {
        'title': '/html/head/title',
        'price': '/html/body/div/div[3]/div[2]/div[1]/div[2]/div/div[2]/div/span/span/span[2]',
        'img': '/html/body/div/div[3]/div[2]/div[1]/div[1]/div/ul/li[1]/img'
    }
    return json.dumps(json_data, indent="\t")


def extract_product():
    """
    :param:
    :return:
    """
    st = timer()
    total = 0
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                              options=options)
    driver.implicitly_wait(5)
    # driver.get("https://m.gmarket.co.kr")
    # todo : Please Parsing Here.
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000174&categoryLevel=1")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000135&categoryLevel=1")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000136&categoryLevel=1")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000137&categoryLevel=1")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal")
    url_list = "https://m.gmarket.co.kr/n/superdeal?categoryCode=400000{}&categoryLevel=1"
    # cateorty_id = [135,136,137,139,140,143,146,148,149,151,152,174]
    cateorty_id = [174, 136]

    print("-->", timedelta(seconds=timer() - st))
    # Todo : 각 리스트 별로 함수화해서 분산 처리해야할 듯
    # Selenium
    # elements = driver.find_elements_by_xpath('//*[@class="component"]')
    # print(len(elements))

    import motor.motor_asyncio
    host = "localhost"
    port = 27017
    client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    async def extract_element(ele):
        try: #div/div/
            el_img = ele.find_element_by_xpath('//div[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img')
            el_price = ele.find_element_by_xpath('//div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong')
            el_url = ele.find_element_by_xpath('//div[@class="box__itemcard-superdeal--img"]/a')
            # await mongo.insert_doc({
            #     "title": el_img.get_attribute("alt"),
            #     "price": el_price.text,
            #     "img": el_img.screenshot_as_base64,
            #     "url": el_url.get_property("href")
            # }, "shop_db", "test")
            # await print(el_img.get_attribute("alt"))
            # await print(el_img.screenshot_as_base64)
            # await print(el_price.text)
            # await print(el_url.get_property("href"))
            return {
                "title": el_img.get_attribute("alt"),
                "price": el_price.text,
                # "img": el_img.screenshot_as_base64,
                "url": el_url.get_property("href")
            }

        except Exception as e:  # ㅜ
            print(e)

    async def gather_extract(url):
        # driver = webdriver.Chrome(executable_path="./chromedriver.exe",
        #                           options=options)
        # driver.implicitly_wait(2)

        driver.get(url)
        elements = driver.find_elements_by_xpath('//*[@class="component"]')
        print(url, len(elements))
        if len(elements) != 0:
            return await asyncio.gather(*[extract_element(el) for el in elements])
            # print(res)
            # return [await extract_element(el) for el in elements]
            # for ele in elements:
            #     try:
            #         el_img = ele.find_element_by_xpath(
            #             'div/div/div[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img')
            #         el_price = ele.find_element_by_xpath(
            #             'div/div/div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong')
            #         el_url = ele.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a')
            #
            #         await mongo.insert_doc({
            #             "title": el_img.get_attribute("alt"),
            #             "price": el_price.text,
            #             "img": el_img.screenshot_as_base64,
            #             "url": el_url.get_property("href")
            #         }, "shop_db", "test")
            #     except Exception:
            #         pass

    async def main(url):
        res = await asyncio.gather(*[gather_extract(url.format(str(i))) for i in cateorty_id])
        print(res)

    t = timer()
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(main(url_list))
    loop.close()
    print("Async -->", timedelta(seconds=timer() - t))
    driver.quit()

    return total


if __name__ == '__main__':
    st = timer()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    print("Total :", extract_product())
    # make_dynamic_xpath()
    print("실행 시간", timedelta(seconds=timer() - st))


"""
def extract_product():
    st = timer()
    total = 0
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                              options=options)
    driver.implicitly_wait(2)
    # driver.get("https://m.gmarket.co.kr")
    # todo : Please Parsing Here.
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000174&categoryLevel=1")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000135&categoryLevel=1")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000136&categoryLevel=1")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    # driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000137&categoryLevel=1")
    # raw_html = driver.page_source
    # html = BeautifulSoup(raw_html, 'html.parser')
    # li_size = len(html.find_all("div", attrs={'class': 'component'}))
    # print(">>", li_size)
    # total += li_size
    # time.sleep(0.1)
    driver.get("https://m.gmarket.co.kr/n/superdeal")
    raw_html = driver.page_source
    print("-->", timedelta(seconds=timer() - st))
    # Todo : 각 리스트 별로 함수화해서 분산 처리해야할 듯
    # Selenium
    import base64

    elements = driver.find_elements_by_xpath('//*[@class="component"]')
    print(len(elements))
    for el in elements:
        el_img = el.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img')
        el_price = el.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong')
        el_url = el.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a')

        print(el_img.get_attribute("alt"))
        print(el_price.text)
        print(el_img.screenshot_as_base64)
        print(el_url.get_property("href"))

    print("-->", timedelta(seconds=timer() - st))

    # Using BS4
    html = BeautifulSoup(raw_html, 'html.parser')
    data = html.find_all("div", attrs={'class': 'component'})
    li_size = len(data)
    # print(data)
    print(">>", li_size)
    total += li_size
    print("-->", timedelta(seconds=timer() - st))
    driver.quit()
    # driver.close()
    return total
    
    elements = driver.find_elements_by_xpath('//*[@class="component"]')
    print(len(elements))
    t1 = timer()
    for el in elements:
        el_img = el.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img')
        el_price = el.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong')
        el_url = el.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a')
        # time.sleep(0.05)
        # print(el_img.get_attribute("alt"))
        # print(el_price.text)
        # print(el_img.screenshot_as_base64)
        # print(el_url.get_property("href"))

    print("Sync -->", timedelta(seconds=timer() - t1))

    async def extract_element(ele):
        el_img = ele.find_element_by_xpath(
            'div/div/div[@class="box__itemcard-superdeal--img"]/a/div[@class="box-product"]/span[@class="box-product__img-product"]/img')
        el_price = ele.find_element_by_xpath(
            'div/div/div[@class="box__itemcard-superdeal--info"]/a/div[@class="box__itemcard--price"]/span/strong')
        el_url = ele.find_element_by_xpath('div/div/div[@class="box__itemcard-superdeal--img"]/a')
        # await asyncio.sleep(0.05)
        # print(el_img.get_attribute("alt"))
        # print(el_price.text)
        # print(el_img.screenshot_as_base64)
        # print(el_url.get_property("href"))

    async def main(elements):
        await asyncio.gather(*[extract_element(el) for el in elements])

    t2 = timer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(elements))
    loop.close()
    print("Async -->", timedelta(seconds=timer() - t2))

    driver.quit()
    return total
    """

