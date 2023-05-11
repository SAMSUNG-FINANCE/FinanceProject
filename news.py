from selenium import webdriver
import time
from selenium.webdriver.common.by import By
# WebDriver 객체 생성
driver = webdriver.Chrome()

# 네이버 증권 삼성전자 뉴스 페이지 접속
url = "https://m.stock.naver.com/domestic/stock/005930/news/title"
driver.get(url)
driver.implicitly_wait(10)
# 뉴스 기사들을 순회하면서 클릭
news_links =driver.find_elements(By.CSS_SELECTOR,"#content > div:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div.NewsList_article__2hkCL > ul")


for news_link in news_links:
    
    # 뉴스 기사 링크 클릭
    news_link.click()
    
    # 새로운 탭으로 전환
    driver.switch_to.window(driver.window_handles[-1])
    
    # 기사 제목과 내용 출력
    news_title = driver.find_element(By.TAG_NAME,"strong").text
    print("제목:", news_title)

    root_div = driver.find_element(By.TAG_NAME, "div")
    content_box_div = root_div.find_element(By.CLASS_NAME, "NewsEnd_contentBox__R7Ics")
    print(content_box_div.text)
    # news_content = driver.find_element(By.CSS_SELECTOR,"div.articleCont").text

    # print("내용:", news_content)
    
    # 기사 내용 출력 후 다시 원래 탭으로 전환
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    
    # 다음 뉴스 기사로 이동
    driver.execute_script("arguments[0].scrollIntoView();", news_link)
    driver.execute_script("window.scrollBy(0, -150);")
    time.sleep(1)
