import sys    # 시스템
import os     # 시스템

import pandas as pd    # 판다스 : 데이터분석 라이브러리
import numpy as np     # 넘파이 : 숫자, 행렬 데이터 라이브러리

from bs4 import BeautifulSoup     # html 데이터 전처리
from selenium import webdriver    # 웹 브라우저 자동화
import time                       # 시간 지연
from tqdm import tqdm_notebook    # 진행상황 표시

address_list = [] #주소
text_list = [] # 대
deal_list = [] # 거래 방식
won_list = [] # 가격
kind_list = [] # 토지
area_list = [] # 면적

### step 1. 부동산 크롤링
# 크롬 웹브라우저 실행
driver = webdriver.Chrome(r"C:\Users\USER\Desktop\chromedriver_win32\chromedriver.exe")

# 사이트 주소
driver.get("https://new.land.naver.com/offices?ms=36.3615444,127.3784552,14&a=SG:SMS:GJCG:APTHGJ:GM:TJ&e=RETAIL")
time.sleep(2)

# 토지 클릭
driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/a[4]/span/em[4]").click()
time.sleep(1)

driver.find_element_by_css_selector(".filter_btn_select").click()
driver.find_element_by_xpath("/html/body/div[2]/div/section/div[1]/div/div[1]/div/div[1]/div/ul/li[2]/label").click()
driver.find_element_by_css_selector(".btn_close").click()

# 상가, 사무실, 공장/창고, 지식산업센터, 건물 클릭으로 해제
driver.find_element_by_css_selector("#type0").click()
driver.find_element_by_css_selector("#type1").click()
driver.find_element_by_css_selector("#type2").click()
driver.find_element_by_css_selector("#type3").click()
driver.find_element_by_css_selector("#type4").click()
time.sleep(1)

# 시 클릭
driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/a/span[1]").click()
time.sleep(0.5)

# 대전시 클릭
driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[5]/label").click()
time.sleep(0.5)

# 구 목록 가져오기
address1 = driver.find_element_by_css_selector(".area_list--district").text.split()

# 구 클릭
for i1 in range(1, len(address1)+1):
    time.sleep(0.5) 
    #element1 = "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/div/div[2]/ul/li[{}]/label".format(i1)
    element1 = "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[{}]/label".format(i1)
    driver.find_element_by_xpath(element1).click()
    time.sleep(0.5)
    
    # 동 목록 가져오기
    address2 = driver.find_element_by_css_selector(".area_list--district").text.split()

    # 동 클릭
    for i2 in range(1, len(address2)+1):
        #element2 = "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/div/div[2]/ul/li[{}]/label".format(i2)
        element2 = "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[{}]/label".format(i2)
        driver.find_element_by_xpath(element2).click()
        time.sleep(1)
    
        # 크롤링
        item = driver.find_element_by_css_selector(".item_list.item_list--article").text

        item_text = item.split('\n')

        ok_num = list(filter(lambda x: ('m²' in item_text[x]), range(len(item_text))))

        # 대
        for i in ok_num:
            text_list.append(item_text[i-2])

        # 거래 방식
        for i in ok_num:
            deal_list.append(item_text[i-1][0:2])

        # 가격
        for i in ok_num:
            price = item_text[i-1][2:]
            # 가격에 억 이하 단위가 없을 시 0000 삽입
            if price[-1] =='억':
                price = price + '0000'

            # (억 , 띄워쓰기) 제거
            won = ''.join( x for x in price if x not in '억, ')
            # 원 단위로 변환
            won += '0000'
            won_list.append(int(won))

        # 토지
        for i in ok_num:
            kind_list.append(item_text[i][0:2])

        # 면적
        for i in ok_num:
            area = item_text[i][2:-2]
            area_list.append(int(area))
        
        # 주소 저장
        address = address1[i1-1], address2[i2-1]
        for i in ok_num:
            address_list.append(address)

        print(address1[i1-1], address2[i2-1], len(address_list), len(text_list), len(deal_list), len(won_list), len(kind_list), len(area_list))
    
        driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/a/span[3]").click()
        
    time.sleep(0.5)
    driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/a/span[2]").click()
    time.sleep(0.5)
    driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/a/span[2]").click()
    
df = pd.DataFrame({'주소':address_list, '구분':text_list, '거래방식':deal_list, '가격':won_list, '대지형태':kind_list, '면적':area_list})
df

df.info()

df.to_excel('crawler_naver 부동산.xlsx')