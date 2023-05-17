import selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import time
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
warnings.filterwarnings('ignore')


path="https://markets.hankyung.com/stock/005930"

driver = webdriver.Chrome()
driver.get(path)

#페이지 로딩 될 때까지 대기
driver.implicitly_wait(10)

# 종목
title=driver.find_element(By.CLASS_NAME,'ellip')
print(title.text)


# PER, EPS, 주당배당금, 배당성향, 시가 총액, 상장 주식수
elements = driver.find_elements(By.CSS_SELECTOR, "#container > div > div > div.stock-view-container > section.stock-view-content > div.stock-view-all > div.container-inner > div > div.aside > div.aside-module.aside-box > div:nth-child(2) > div:nth-child(3) > div > dl:nth-child(n) > dd > strong:nth-child(n)")
for element in elements:
    print(element.text)

# 컨센서스 칸이동
consensus_click=driver.find_element(By.CSS_SELECTOR,"#container > div > div > div.stock-view-container > section.stock-view-content > div.tab-wrap.tab-type2-wrap.container-inner > ul > li:nth-child(3) > a")
href = consensus_click.get_attribute("href")
print(href)

consensus_click.click()

# 투자의견, 종가, 목표가
elements=driver.find_elements(By.CSS_SELECTOR,"#container > div > div > div.stock-view-container > section.stock-view-content > div.stock-view-consensus > div > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(n) > td > strong")
for element in elements:
    print(element.text)




time.sleep(10) 
driver.quit() 