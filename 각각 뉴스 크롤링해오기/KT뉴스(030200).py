from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl
import re


wb=openpyxl.Workbook()
sheet=wb.active

sheet.append(["KT 뉴스 제목","KT 뉴스 본문"])

# WebDriver 객체 생성
driver = webdriver.Chrome()

# 네이버 증권 KT 뉴스 페이지 접속
url = "https://m.stock.naver.com/domestic/stock/030200/news/title"
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
                sheet.append([news_title,news_content])
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
                    sheet.append([news_title,news_content])
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


wb.save(filename='KT 기사 스크래핑.xlsx')
driver.quit()