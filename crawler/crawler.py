import import_ipynb
from tqdm import tqdm

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from save_files import save_json, load_json
import sys

KEY_WORDS = [('인물',18507),('지명',3701),('개념용어',6421),('문화재',7088),('유물',2452),('단체',5746),('작품',4542),('문헌',11856),('사건',1133),('물품',1504),('제도',6617),('놀이',226),('유적',8094),('의식행사',728),('동식물',1628)]
#KEY_WORD_SIZE = [18507, 3701, 6421, 7088, 2452, 5746, 4542, 11856, 1133, 1504, 6617, 226, 8094, 728, 1628]
URL = 'http://encykorea.aks.ac.kr/Contents/CategoryNavi?category=contenttype&keyword={0}&ridx={1}&tot={2}'

def start_crawling(number):
    driver = webdriver.Chrome('chromedriver.exe')
    
    korean_json = None #will save at json
    korean_histories = None #will save at list in json
    current_len = 0
    
    try:
        korean_json = load_json('history_{0}.json'.format(number))
        korean_histories = korean_json['list']
        current_len = len(korean_histories)
    except:
        korean_json = dict()
        korean_histories = []
    
    keyword = KEY_WORDS[number][0]
    size = KEY_WORDS[number][1]

    size_cnt = current_len
    while size_cnt < size:
        title = ''
        cat_and_vals = []
        bodies = []
        document = ''

        url_ = URL.format(keyword, size_cnt, size) # define url
        driver.get(url_)
        driver.implicitly_wait(time_to_wait=1000)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            title = soup.select('#ko_title')[0].get_text()
            cats = soup.select('#cm_meta > div > dl > dt') #categorys
            vals = soup.select('#cm_meta > div > dl > dd') #values

            document += '제목 : {0} / '.format(title)

            for intro_cnt in range(len(cats)):
                cat = cats[intro_cnt].string
                val = vals[intro_cnt].string
                if val == None: #if val have child elem
                    vals[intro_cnt].a.dl.decompose() #delete child elem
                    val = vals[intro_cnt].a.string
                document += '{0} : {1} / '.format(cat, val)
                cat_and_vals.append((cat, val))
            content_headers = soup.select('#cntsWrap > div.contents > div.wrap > div.cnt_dtis > strong.dti_tit')
            contents = soup.select('#cntsWrap > div.contents > div.wrap > div.cnt_dtis > div.dti_cont')
            for cont_cnt in range(len(content_headers)):
                header = content_headers[cont_cnt].get_text().strip()
                content = contents[cont_cnt].get_text().strip()
                document += '{0} : {1} / '.format(header, content)
                bodies.append((header, content))
            korean_history = dict()
            korean_history['title'] = title
            korean_history['intro'] = cat_and_vals
            korean_history['content'] = bodies 
            korean_history['document'] = document
            korean_histories.append(korean_history)
            korean_json['list'] = korean_histories
            save_json('history_{0}.json'.format(str(number)), korean_json)
            size_cnt += 1
        except Exception as ex:
            print(ex)
            print(url_)
            continue
    driver.close()

