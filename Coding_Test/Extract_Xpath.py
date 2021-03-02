from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json


def make_dynamic_xpath(url, title, price, img):
    """
    :param: URL, Title, Price, Img
    :return: Xpath as Json
    """
    print(". . .")
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                              options=options)
    driver.implicitly_wait(2)
    # url = 'http://mitem.gmarket.co.kr/Item?goodscode=1307494915'
    # title = '2080 키즈 어린이치약 그린애플 100g 9개'
    # price = '일시품절'
    # img = 'http://gdimg.gmarket.co.kr/1307494915/still/400?ver=1602832552'
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
        try:
            child = element if element.name else element.parent
            for parent in child.parents:  # parent: bs4.element.Tag
                previous = itertools.islice(parent.children, 0, parent.contents.index(child))
                xpath_tag = child.name
                xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
                components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
                child = parent
            components.reverse()
        except Exception as e:
            print("Error: ", e)
        return '/%s' % '/'.join(components)

    raw_html = driver.page_source
    soup = BeautifulSoup(raw_html, 'lxml')
    img_xpath = xpath_soup(soup.find(attrs={'src': img}))
    title_xpath = xpath_soup(soup.find(text=re.compile(title)))
    price_xpath = xpath_soup(soup.find(text=re.compile(price)))  # re.complie(price) OK But [] No
    driver.quit()
    xpath_json = {
        'title': title_xpath,
        'price': price_xpath,
        'img': img_xpath
    }

    return json.dumps(xpath_json, indent="\t")


if __name__ == '__main__':
    while 1:
        url = input("상품 URL 입력: ")
        title = input("상품 이름 입력: ")
        price = input("상품 가격 입력: ")
        img = input("상품 이미지 입력: ")
        print("\nXpath Json: ", make_dynamic_xpath(url, title, price, img))
