from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer
from datetime import timedelta
import requests, pprint, datetime, json, time

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
    url = 'http://mitem.gmarket.co.kr/Item?goodscode=1307494915'
    title = '2080 키즈 어린이치약 그린애플 100g 9개'
    price = '일시품절'
    img = 'http://gdimg.gmarket.co.kr/1307494915/still/400?ver=1602832552'
    driver.get(url)

    import itertools
    # import re

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
    driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000138&categoryLevel=1")
    raw_html = driver.page_source
    print("-->", timedelta(seconds=timer() - st))
    # Todo : 각 리스트 별로 함수화해서 분산 처리해야할 듯
    # Selenium
    component_list = list(map(lambda x: x.text, driver.find_elements_by_xpath('//*[@class="component"]')))
    price_list = list(map(lambda x: x.text, driver.find_elements_by_xpath('//*[@class="text__price"]')))
    title_list = list(map(lambda x: x.text, driver.find_elements_by_xpath('//*[@class="text__title"]')))
    url_list = list(map(lambda x: x.get_attribute('href'), driver.find_elements_by_xpath('//div[@class="box__itemcard-superdeal--inner"]//div[@class="box__itemcard-superdeal--img"]//*[@class="box__itemcard-superdeal--link"]')))
    d = driver.find_elements_by_xpath('//*[@class="box-product__img-product"]/img')  # 이미지는 a.screenshot("./a.jpg")) 와 같이
    print(price_list, title_list, url_list, len(price_list), len(title_list), len(component_list), len(url_list))
    # for i in range(0, len(b)):
    #     print(list(zip(b[i].text, c[i].text)))
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


if __name__ == '__main__':
    st = timer()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    print("Total :", extract_product())
    # make_dynamic_xpath()
    print("실행 시간", timedelta(seconds=timer() - st))


