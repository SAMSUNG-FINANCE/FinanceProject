import selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import time
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
warnings.filterwarnings('ignore')

 # 데이터프레임 생성
df = pd.DataFrame(columns=['ID','종목','per', 'eps', '주당배당금', '배당성형', '시가총액', '상장주식수'])
df2=pd.DataFrame(columns=['ID','투자의견','종가','목표가'])

code={'삼성전자': '005930',
      'LG에너지솔루션': '373220',
      'SK하이닉스':'000660',
      '삼성바이오로직스':'207940',
      'LG화학':'051910',
      '현대차':'005380',
      'NAVER':'035420',
      '셀트리온':'068270',
      '삼성물산':'028260',
      '하이브':'352820',
      '대한항공':'003490',
      '카카오페이':'377300',
      '한국전력':'015760',
      '엔씨소프트':'036570',
      'CJ제일제당':'097950',
      '한미약품':'128940',
      'POSCO홀딩스':'005490',
      'S-oil':'010950'}
for idx, company in enumerate(code):
    path="https://markets.hankyung.com/stock/"+code[company]
    print(path)

    driver = webdriver.Chrome()
    driver.get(path)

   
    #페이지 로딩 될 때까지 대기
    driver.implicitly_wait(10)

    # 종목
    title=driver.find_element(By.CLASS_NAME,'ellip')
    print(title.text)


    # PER, EPS, 주당배당금, 배당성향, 시가 총액, 상장 주식수
    root_div=driver.find_element(By.TAG_NAME,"div")
    elements=driver.find_elements(By.CLASS_NAME,"define-list")
    for idx2,element in enumerate(elements):
        item=element.find_element(By.TAG_NAME,"strong")
        print(item.text)
        if(idx2==0):
            per_value=item.text
        elif(idx2==1):
            eps_value=item.text
        elif(idx2==2):
            dividend_value=item.text
        elif(idx2==3):
            payout_ratio_value=item.text
        elif(idx2==4):
            market_cap_value=item.text
        elif(idx2==5):
            shares_outstanding_value=item.text
    print(idx)
    df.loc[idx]=[idx,company,per_value,eps_value,dividend_value,payout_ratio_value,market_cap_value,shares_outstanding_value]
    print(df)
    
    # 컨센서스 칸이동
    consensus_click=driver.find_element(By.CSS_SELECTOR,"#container > div > div > div.stock-view-container > section.stock-view-content > div.tab-wrap.tab-type2-wrap.container-inner > ul > li:nth-child(3) > a")
    consensus_click.click()

    # 투자의견, 종가, 목표가
    root_td=driver.find_elements(By.TAG_NAME,"td")
    for idx3,item in enumerate(root_td):
        target=item.find_element(By.TAG_NAME,"strong")
        print(target.text)
        if(idx3==0):
            invest_opinion_value=target.text
        elif(idx3==1):
            end_value=target.text
        elif(idx3==2):
            goal_value=target.text
    print(idx)
    df2.loc[idx]=[idx,invest_opinion_value,end_value,goal_value]
    print(df2)
    

time.sleep(10) 
driver.quit() 

merged_df=pd.merge(df,df2,on='ID')
print(merged_df)

merged_df.to_csv('data.csv',index=False)