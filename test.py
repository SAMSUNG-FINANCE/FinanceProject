import requests
from bs4 import BeautifulSoup

url = 'https://markets.hankyung.com/stock/005930/financial-summary'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.find('tr').get_text())  #기업가치분석
    print(soup.find('tbody').get_text()) #기업가치분석
    # print(soup.find_all('td').get_text())  # 기업가치분석
    results = soup.find_all("td")
    for result in results:
        text = result.get_text()
        print(text)

else:
    print(response.status_code)