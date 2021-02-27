from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer
from datetime import timedelta
import requests, pprint, datetime, json, time,unittest

"""
    selenium의 webdriver를 사용하기 위해선 크롬 버전에 맞는 chromedriver.exe가 필요하다
    Options의 headless = True는 브라우져를 렌더링하지 않고 메모리 상에서만 작업하도록 하는 옵션.
    자바스크립트 페이지 로딩이 끝날 때 까지 기다리는 방법.
    Driver의 execution_script() 함수로 자바스크립트 함수 실행을 할 수 있다.

    Page의 단일 Element에 접근하는 Method
    find_element_by_name('HTML_name')
    find_element_by_id('HTML_id')
    find_element_by_xpath('/html/body/some/xpath')
    find_element_by_css_selector('#css > div.selector')
    find_element_by_class_name('some_class_name')
    find_element_by_tag_name('h1')

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
"""


class Crawling_Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    @staticmethod
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
        driver.get("https://m.gmarket.co.kr/n/superdeal?categoryCode=400000138&categoryLevel=1")
        raw_html = driver.page_source
        print("-->", timedelta(seconds=timer() - st))
        # Selenium
        b = driver.find_elements_by_xpath('//*[@class="text__price"]')
        c = driver.find_elements_by_xpath('//*[@class="text__title"]')
        d = driver.find_elements_by_xpath('//*[@class="box-product__img-product"]/img') # 이미지는 a.screenshot("./a.jpg")) 와 같이
        # for a in b:
        #     print(a.text)
        print(list(map(lambda x: x.text, b)))
        import cv2, base64
        cv = cv2.imread("./test.png")
        bcv = cv2.imencode('.PNG', cv)[1].tobytes()
        print(bcv, type(bcv))

        with open('test.png', "rb") as f:
            print("\n", base64.b64encode(f.read()), type(base64.b64encode(f.read())))

        with open('test.png', "rb") as f:
            print("\n", bytearray(f.read())[0], type(bytearray(f.read())[0]))
        # for i in range(0, len(b)):
        #     print(list(zip(b[i].text, c[i].text)))
        print("-->", timedelta(seconds=timer() - st))
#
        # Using BS4
        html = BeautifulSoup(raw_html, 'html.parser')
        data = html.find_all("div", attrs={'class': 'component'})
        li_size = len(data)
        # print(data)
        print(">>", li_size)
        total += li_size
        print("-->", timedelta(seconds=timer() - st))
        driver.quit()

        return total

    def tearDown(self):
        self.driver.close()


def extract_xpath_from_product():
    url = 'http://www.gsshop.com/prd/prd.gs?prdid=37216130',
    title = '[애플망고]딥브이원피스'
    price = '8,010'
    img = 'http://image.gsshop.com/image/37/21/37216130_L1.jpg'

    json_data = {
        'title': '/html/head/title',
        'price': '/html/body/div/div[3]/div[2]/div[1]/div[2]/div/div[2]/div/span/span/span[2]',
        'img': '/html/body/div/div[3]/div[2]/div[1]/div[1]/div/ul/li[1]/img'
    }
    print(type(json_data))
    return json.dumps(json_data, indent="\t")


if __name__ == '__main__':
    # unittest.main()
    st = timer()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    print("Total :", Crawling_Test.extract_product())
    # res = extract_xpath_from_product()
    # print(res, type(res), len(res))
    # print(json.loads(res), type(json.loads(res)))
    print("실행 시간", timedelta(seconds=timer() - st))


