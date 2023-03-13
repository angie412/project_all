from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Chrome 브라우저를 띄우지 않고 실행하는 옵션 설정
#options = Options()
#options.headless = True
#options.add_argument("window-size=1920x1080")

# Chrome 브라우저 실행
#driver = webdriver.Chrome('chromedriver.exe', options=options)
path = "C:/Users/USER/Desktop/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(path)


url = "https://new.land.naver.com/offices?ms=37.564423,127.1488659,12&a=SG:SMS:GJCG:APTHGJ:GM:TJ&e=RETAIL"
time.sleep(2) 
driver.get(url)
time.sleep(2)
# 가져올 페이지 URL
#url = 'https://land.naver.com/article/articleList.nhn?rletTypeCd=B02&tradeTypeCd=&hscpTypeCd=B02%3AB03%3AB01&cortarNo=1168010800&articleOrderCode=&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrice=&maxPrice=&minPrice1=&maxPrice1=&minArea=&maxArea=&minFloor=&maxFloor=&minRooms=&maxRooms=&startDate=&endDate=&order=point_&showR0=N&page={}'

# 가져올 페이지 수
page_count = 5

# 결과를 저장할 빈 리스트
results = []

for page in range(1, page_count + 1):
    # 페이지 URL을 완성
    page_url = url.format(page)
    
    # 페이지 접속
    driver.get(page_url)
    
    # 페이지 HTML 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # 상가 매물 정보가 담겨 있는 테이블을 찾음
    table = soup.find('table', {'class': 'sale_list _tb_site_img NE=a:lst'})
    
    # 테이블에서 각 행을 찾아서 결과 리스트에 추가
    for tr in table.find_all('tr', {'class': 'sale_item'}):
        row = []
        # 각 컬럼을 찾아서 row 리스트에 추가
        for td in tr.find_all('td'):
            row.append(td.text.strip())
        results.append(row)
    
# Chrome 브라우저 종료
driver.quit()

# 결과를 데이터프레임으로 변환하여 출력
df = pd.DataFrame(results, columns=['거래', '면적', '가격', '동', '층', '용도', '도로명'])
print(df)
