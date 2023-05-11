import selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import time
import warnings
warnings.filterwarnings('ignore')


path="https://markets.hankyung.com/stock/005930"

driver = webdriver.Chrome()

driver.get(path)


# aside=driver.find_element(By.CLASS_NAME,'aside')
# print(elements.text)

title=driver.find_element(By.CLASS_NAME,'ellip')
print(title.text)

# elements = driver.find_elements(By.CSS_SELECTOR, '.change_rate_detail .define-list .txt-num')
# for element in elements:
#     print(element.text)


time.sleep(10) 
driver.quit() 