from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from elasticsearch import Elasticsearch, helpers
from multiprocessing import Pool, cpu_count
from itertools import repeat
import pandas as pd
import requests, pprint, time, datetime

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
"""


def get_html(_url, _id):
    def make_index(_es, name):
        if es.indices.exists(index=name):
            # es.indices.delete(index=name)
            pass
        print(es.indices.create(index=name))

    es = Elasticsearch(["13.125.246.197", "52.79.215.253", "52.79.250.228"],
                       http_auth=('elastic', 'rkwjs12#'),
                       port=9200)
    print(es.info())
    make_index(es, ID_TO_MANUFACTURE[_id])
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                              options=options)
    driver.implicitly_wait(3)
    driver.get(_url + _id)
    time.sleep(3)
    if type(_url) is str and type(_id) is str:
        # raw_html = requests.get(_url + _id)
        # html = BeautifulSoup(raw_html.content, 'html.parser')
        raw_html = driver.page_source
        html = BeautifulSoup(raw_html, 'html.parser')
        li_size = len(html.find_all("li", attrs={'class': 'thumb_nail'}))
        pagination_size = html.find("div", attrs={'id': '_review_paging'})
        if not li_size:
            print("상품 정보가 없습니다.")
            driver.close()
            raise Exception
        if pagination_size is None:
            pagination_size = 1
        else:
            pagination_size = int(
                "".join(filter(str.isdigit, html.select_one("#_review_paging > a.next_end").attrs['onclick'])))
        crawling_arr_set = []
        print("Page Size : ", pagination_size)
        i = 1
        while pagination_size >= i:
            raw_html = driver.page_source
            html = BeautifulSoup(raw_html, 'html.parser')
            li_size = len(html.find_all("li", attrs={'class': 'thumb_nail'}))
            print()
            while li_size:
                #print("Index : ", ID_TO_MANUFACTURE[_id], "li size : ", li_size, "  Page : ", i)
                average_star = html.select_one(
                    "#_review_list > li:nth-child(%d) > div > div.avg_area > a > span.curr_avg > strong" % li_size).text
                store = html.select_one(
                    "#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(1)" % li_size).text
                user_name = html.select_one(
                    "#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(2)" % li_size).text
                write_date = html.select_one(
                    "#_review_list > li:nth-child(%d) > div > div.avg_area > span > span:nth-child(3)" % li_size).text
                title_text = html.select_one("#_review_list > li:nth-child(%d) > div > p > strong" % li_size).text
                body_text = html.select_one("#_review_list > li:nth-child(%d) > div > div.atc" % li_size).text
                low_price = html.select_one('#content > div > div.summary_cet > div.price_area > span > em').text
                feature = html.select_one(
                    '#container > div.summary_area > div.summary_info._itemSection > div > div.goods_info > div.info_inner.list').text
                manufacturer = html.select_one(
                    '#container > div.summary_area > div.summary_info._itemSection > div > div.goods_info > div:nth-child(1) > span:nth-child(1) > em').text
                source = {
                    "manufacturer": manufacturer,
                    "aver_star": average_star,
                    "price": low_price,
                    "feature": str(feature).replace("\n", ""),
                    "user": user_name,
                    "store": store,
                    "date": datetime.datetime.strptime(write_date, '%y.%m.%d.'),
                    "title": str(title_text).replace("\n", ""),
                    "body": str(body_text).replace("\n", ""),
                    "product_id": _id,
                    "page": i,
                    "col": li_size
                }
                crawling_arr_set.append(source)
                # Elastic Input
                body = [
                    {
                        "_index":  ID_TO_MANUFACTURE[_id],
                        "_source": source
                    }
                ]
                helpers.bulk(es, body)
                li_size -= 1
            i += 1
            driver.execute_script("shop.detail.ReviewHandler.page(%d, '_review_paging');" % i)
            time.sleep(0.2)
    else:
        print("올바른 스트링 타입이 아닙니다.")
        driver.close()
        raise Exception
    driver.close()
    return crawling_arr_set


# Macro
REVIEW_SELECTOR_PRE = "#_review_list > li:nth-child"
REVIEW_SELECTOR_MID = " > div > div.avg_area > span > "
# Naver Shopping
# https://search.shopping.naver.com/search/all?frm=NVSHMDL&productSet=model&query=공기청정기
NAVER_SHOPPING_BASE_URL = "https://search.shopping.naver.com/detail/detail.nhn?nvMid="
KUKU_AC_25W20FPMO = "21076849694"
DYSON_PURE_COOL_TP_04 = "13810664630"
ITC_PURIWAY_PW_150 = "20850829749"
LG_PURICARE_AS300DWFA = "21285691276"
WINIX_FRIME_APRM833_JWK = "21393999339"
SAMSUNG_BLUESKY_AX34N3020WWD = "13611653308"
SKMAGIC_ACL_120Z0 = "17586234530"
ELECTROMAN_DAP_2215NAWHEM = "22163383505"

WAYCOS_THINKAIR_AD12C = "21060688821"
DAEWOOGLOBAL_GRUENLUFT_HM_8000PULS = "12830002273"
WINIX_ZEROS_AZSE430_JWK = "21106741445"
OA_OA_HM230 = "12340177564"
SAMJI_IT_PISNET_PURE360 = "12861463404"
SAMSUNG_BLUESKY_AX60N5580WDD = "12624200918"
KUKU_AC_12X20FW = "11701776972"
XIAOMI_MIAIR_2S = "13689762877"
XIAOMI_MIAIR_2 = "11307320311"
AIRVITA_DUSTZERO = "13371199127"

# Name Definition : review_ + Manufacture_ + Model Name
ID_TO_MANUFACTURE = {
    "21076849694": "review_kuku_ac_25w20fpmo",
    "13810664630": "review_dyson_pure_cool_tp_04",
    "20850829749": "review_itc_puriway_pw_150",
    "21285691276": "review_lg_puricare_as300dwfa",
    "21393999339": "review_winix_frime_aprm833_jwk",
    "13611653308": "review_samsung_bluesky_ax34n3020wwd",
    "17586234530": "review_skmagic_acl_120z0",
    "22163383505": "review_electroman_dap_2215nawhem",

    "21060688821": "review_waycos_thinkair_ad12c",
    "12830002273": "review_daewooglobal_gruenluft_hm8000puls",
    "21106741445": "review_winix_zeros_azse430_jwk",
    "12340177564": "review_oa_oa_hm230",
    "12861463404": "review_samji_it_pisnet_pure360",
    "12624200918": "review_samsung_bluesky_ax60n5580wdd",
    "11701776972": "review_kuku_ac_12x20fw",
    "13689762877": "review_xiaomi_miair_2s",
    "11307320311": "review_xiaomi_miair_2",
    "13371199127": "review_airvita_dustzero"
}

product_arr = [KUKU_AC_25W20FPMO, DYSON_PURE_COOL_TP_04, ITC_PURIWAY_PW_150, LG_PURICARE_AS300DWFA,
               WINIX_FRIME_APRM833_JWK, SAMSUNG_BLUESKY_AX34N3020WWD, SKMAGIC_ACL_120Z0, ELECTROMAN_DAP_2215NAWHEM,
               WAYCOS_THINKAIR_AD12C, DAEWOOGLOBAL_GRUENLUFT_HM_8000PULS, WINIX_ZEROS_AZSE430_JWK, OA_OA_HM230,
               SAMJI_IT_PISNET_PURE360, SAMSUNG_BLUESKY_AX60N5580WDD, KUKU_AC_12X20FW, XIAOMI_MIAIR_2S, XIAOMI_MIAIR_2,
               AIRVITA_DUSTZERO]

if __name__ == '__main__':
    st = datetime.datetime.now().timestamp()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    pool = Pool(processes=16)
    pool.starmap(get_html, zip(repeat(NAVER_SHOPPING_BASE_URL), product_arr))
    pool.close()
    pool.join()
    gt = datetime.datetime.now().timestamp()

    # Not Use Multiprocessing
    # for product_id in product_arr:
    #     make_index(es, ID_TO_MANUFACTURE[product_id])
    #     res = get_html(NAVER_SHOPPING_BASE_URL, product_id)
    #     dt = datetime.datetime.now().timestamp()
    #     pp.pprint(res)
    #     print(product_id + " Size : ", len(res), "  Time(s) : ", dt - st)
    #     es.indices.refresh(index=ID_TO_MANUFACTURE[product_id])
    #     st = datetime.datetime.now().timestamp()
    #
    print("총 걸린 시간(s) : 약", int(str(int(gt - st))) // 60, "분 ", int(str(int(gt - st))) % 60, "초")
    #raise Exception
