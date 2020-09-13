import requests
from bs4 import BeautifulSoup
import database
import material
import price
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import datetime
from time import sleep



url = 'https://www.tgju.org/'

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=option)

try:
    driver.get(url)
except:
    print('can\'t connect to url.')
    exit(-1)

sleep(5)
table_class_name = 'market-table'


html = driver.page_source
driver.close()
soup = BeautifulSoup(html, 'html.parser')
tables = soup.select(f'.{table_class_name}')

file = open('test', 'w')
for table in tables:
    items = table.select('tbody tr')
    for item in items:
        name = item.find('th').text
        price = item.find('td').text
    
        print(name, price, file=file)

