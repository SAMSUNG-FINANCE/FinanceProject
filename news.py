from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl
import re

name = {
    "LG에너지솔루션": "373220",
    "삼성전자": "005930",
    "SK하이닉스": "000660",
    "삼성바이오로직스": "207940",
    "LG화학": "051910",
    "현대차": "005380",
    "NAVER": "035420",
    "셀트리온": "068270",
    "삼성물산": "028260",
    "하이브": "352820",
    "대한항공": "003490",
    "KT": "030200",
    "카카오페이": "377300",
    "한국전력": "015760",
    "엔씨소프트": "036570",
    "F_F": "383220",
    "CJ제일제당": "097950",
    "한미약품": "128940",
    "POSCO홀딩스": "005490",
    "삼성SDS": "018260",
    "S_oil": "010950"
}
# name["F_F"] = name.pop("F&F")
# name["S_oil"] = name.pop("S-oil")


wb=openpyxl.Workbook()
sheet=wb.active

sheet.append(["종목","제목","본문"])

# WebDriver 객체 생성
driver = webdriver.Chrome()
base_url = "https://m.stock.naver.com/domestic/stock/{}/news/title"
for key,value in name.items():
  # value=int(value)
  #페이지 접속
  url = base_url.format(value)
  driver.get(url)
  driver.implicitly_wait(10)

  # 뉴스 기사들을 순회하면서 클릭
  news_links =driver.find_elements(By.CSS_SELECTOR,"#content > div:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div.NewsList_article__2hkCL > ul > li")

  # 뉴스 개수
  print(len(news_links))
  news_count=0

  count=0

  for idx,news_link in enumerate(news_links):
      # print("현재 뉴스 개수:", news_count)

      # 10개까지만 가져온다
      # if(idx==11):
      #     break
      if count==11:
        break

      try:
          actions = ActionChains(driver)
          actions.move_to_element(news_link) #요소위로 마우스 이동
          actions.click()
          actions.perform()
          
          # news_link.click()

          # 뉴스 제목
          root_div = driver.find_element(By.TAG_NAME, "div")
          news_title = root_div.find_element(By.CLASS_NAME, "NewsHeader_title__1vvDz").text
          print("제목:", news_title)

          # 뉴스 본문
          root_div = driver.find_element(By.TAG_NAME, "div")
          content_box_div = root_div.find_element(By.CLASS_NAME, "NewsEnd_contentBox__R7Ics")
          # news_content = content_box_div.find_element(By.CLASS_NAME, "NewsEnd_textEnd__xIOkX").text
          try:
            news_content = content_box_div.find_element(By.CLASS_NAME, "NewsEnd_textEnd__xIOkX").text
      
          # 정규식을 사용하여 본문의 시작이 [인지 확인
            if not re.match(r"^\[", news_content):
              sheet.append([key,news_title,news_content])
            else:
              count-=1
          except NoSuchElementException:
            count-=1
          print(news_content)

          # sheet.append([news_title,news_content])
          # 이후에 다시 기존 탭으로 전환
          driver.back()
          print("이전 url:", driver.current_url)

          # 다음 뉴스 기사 클릭을 위해 대기
          time.sleep(1)

          news_count += 1
          count+=1
      except StaleElementReferenceException:
          print("StaleElementReferenceException 발생")
          news_links = driver.find_elements(By.CSS_SELECTOR, "#content > div:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div.NewsList_article__2hkCL > ul > li")
          news_link = news_links[news_count]

          actions = ActionChains(driver)
          actions.move_to_element(news_link)
          actions.click()
          actions.perform()

          # news_link.click()
          try: 
              # 뉴스 제목
              root_div = driver.find_element(By.TAG_NAME, "div")
              news_title = root_div.find_element(By.CLASS_NAME, "NewsHeader_title__1vvDz").text
              print("제목:", news_title)

              # 뉴스 본문
              root_div = driver.find_element(By.TAG_NAME, "div")
              content_box_div = root_div.find_element(By.CLASS_NAME, "NewsEnd_contentBox__R7Ics")
              # news_content = content_box_div.find_element(By.CLASS_NAME, "NewsEnd_textEnd__xIOkX").text
              try:
                news_content = content_box_div.find_element(By.CLASS_NAME, "NewsEnd_textEnd__xIOkX").text
      
              # 정규식을 사용하여 본문의 시작이 [인지 확인
                if not re.match(r"^\[", news_content):
                  sheet.append([key,news_title,news_content])
                else:
                  count-=1
              except NoSuchElementException:
                  count-=1
              print(news_content)
    
              # print(news_content)


              # sheet.append([news_title,news_content])
              # 이후에 다시 기존 탭으로 전환
              driver.back()
              print("이전 url:", driver.current_url)

              # 다음 뉴스 기사 클릭을 위해 대기
              time.sleep(1)
          except NoSuchElementException:
              # NoSuchElementException 발생 시 스크롤을 내리고 다시 요소를 찾음
              print("NoSuchElementException 발생")
              driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')




          news_count += 1
          count+=1


wb.save(filename='기사 스크래핑.xlsx')
driver.quit()