from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import requests, pprint, time

"""
    selenium의 webdriver를 사용하기 위해선 크롬 버전에 맞는 chromedriver.exe가 필요하다
    Options의 headless = True는 브라우져를 렌더링하지 않고 메모리 상에서만 작업하도록 하는 옵션.
    자바스크립트 페이지 로딩이 끝날 때 까지 기다리는 방법.
    Driver의 execution_script() 함수로 자바스크립트 함수 실행을 할 수 있다.
"""
options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
driver.implicitly_wait(2)
driver.get("https://search.shopping.naver.com/detail/detail.nhn?nvMid=13611653308")
time.sleep(3)

# URL에 접근하는 Method

"""
# Page의 단일 Element에 접근하는 Method
find_element_by_name('HTML_name')
find_element_by_id('HTML_id')
find_element_by_xpath('/html/body/some/xpath')
find_element_by_css_selector('#css > div.selector')
find_element_by_class_name('some_class_name')
find_element_by_tag_name('h1')
"""

r = requests.get("https://search.shopping.naver.com/detail/detail.nhn?nvMid=13611653308")
html = BeautifulSoup(r.content, 'html.parser')
li_size = len(html.find_all("li", attrs={'class': 'thumb_nail'}))
crawling_arr_set = []
while li_size:
    average_star = html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > a > span.curr_avg > strong" % li_size)[0].text
    store = html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(1)" % li_size)[0].text
    user_name = html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(2)" % li_size)[0].text
    write_date = html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(3)" % li_size)[0].text
    title_text = html.select("#_review_list > li:nth-child(%d) > div > p > strong" % li_size)[0].text
    body_text = html.select("#_review_list > li:nth-child(%d) > div > div.atc" % li_size)[0].text
    # print(li_size)
    # print(average_star, store, user_name, write_date, title_text, body_text)
    crawling_arr_set.append({
        "aver_star": average_star,
        "user": user_name,
        "store": store,
        "date": write_date,
        "title": title_text,
        "body": body_text,
        "product_id": "13611653308"
    })
    li_size -= 1
driver.execute_script("shop.detail.ReviewHandler.page(2, '_review_paging');")
time.sleep(2)

li_size = len(html.find_all("li", attrs={'class': 'thumb_nail'}))
while li_size:
    average_star = html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > a > span.curr_avg > strong" % li_size)[0].text
    store = html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(1)" % li_size)[0].text
    user_name = html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(2)" % li_size)[0].text
    write_date = html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(3)" % li_size)[0].text
    title_text = html.select("#_review_list > li:nth-child(%d) > div > p > strong" % li_size)[0].text
    body_text = html.select("#_review_list > li:nth-child(%d) > div > div.atc" % li_size)[0].text
    # print(li_size)
    # print(average_star, store, user_name, write_date, title_text, body_text)
    crawling_arr_set.append({
        "aver_star": average_star,
        "user": user_name,
        "store": store,
        "date": write_date,
        "title": title_text,
        "body": body_text,
        "product_id": "13611653308"
    })
    li_size -= 1

driver.execute_script("shop.detail.ReviewHandler.page(3, '_review_paging');")
time.sleep(2)

li_size = len(html.find_all("li", attrs={'class': 'thumb_nail'}))
while li_size:
    average_star = \
    html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > a > span.curr_avg > strong" % li_size)[
        0].text
    store = \
    html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(1)" % li_size)[
        0].text
    user_name = \
    html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(2)" % li_size)[
        0].text
    write_date = \
    html.select("#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(3)" % li_size)[
        0].text
    title_text = html.select("#_review_list > li:nth-child(%d) > div > p > strong" % li_size)[0].text
    body_text = html.select("#_review_list > li:nth-child(%d) > div > div.atc" % li_size)[0].text
    # print(li_size)
    # print(average_star, store, user_name, write_date, title_text, body_text)
    crawling_arr_set.append({
        "aver_star": average_star,
        "user": user_name,
        "store": store,
        "date": write_date,
        "title": title_text,
        "body": body_text,
        "product_id": "13611653308"
    })
    li_size -= 1

print(crawling_arr_set, len(crawling_arr_set))
