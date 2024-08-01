#!/usr/bin/env python

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd



driver = webdriver.Chrome()
print(type(driver))
print('-' * 50)

print ('Start~!!')
url = 'https://www.mt.co.kr/ksi/'
driver.get(url)

totscorelist = []
scorelist = []
addrlist = []

select_sido = driver.find_element(By.NAME, 'sido')
select_gugun = driver.find_element(By.NAME, 'gugun')
selgugun = Select(select_gugun)
selsido = Select(select_sido)

for i in range (1, (len(selsido.options))):
    time.sleep(2)
    select_sido = driver.find_element(By.NAME, 'sido')
    selsido = Select(select_sido)
    selsido.select_by_index(i)

    time.sleep(1)
    select_gugun = driver.find_element(By.NAME, 'gugun')
    selgugun = Select(select_gugun)
    for j in range (1, (len(selgugun.options))):
        time.sleep(1)
        select_sido = driver.find_element(By.NAME, 'sido')
        select_gugun = driver.find_element(By.NAME, 'gugun')
        selgugun = Select(select_gugun)
        selsido = Select(select_sido)
        selsido.select_by_index(i)
        selgugun.select_by_index(j)

        time.sleep(1)
        addr = driver.find_element(By.XPATH, '//*[@id="content_title"]/h3').text
        totscore = driver.find_element(By.XPATH, '//*[@id="content_title"]/span').text
        score = driver.find_element(By.XPATH, '//*[@id="content_rank"]').text
        addrlist.append(addr)
        totscorelist.append(totscore)
        scorelist.append(score)
        print(addr)

        driver = webdriver.Chrome()
        url = 'https://www.mt.co.kr/ksi/'
        driver.get(url)

sido = []
gungu = []
rank = []
totscore = []
grade = []

for i in range (len(addrlist)):
    sido.append(addrlist[i].split()[0])
    gungu.append(addrlist[i].split()[1])
    rank.append(addrlist[i].split()[2])

for i in range (len(totscorelist)):
    imsi = totscorelist[i].split('\n')[0]
    totscore.append(imsi.split()[1])
    imsi = totscorelist[i].split('\n')[1]
    grade.append(imsi.split()[1])

mycolumn = ['시도', '군구', '순위', '점수', '등급', '기타']

myframe = pd.DataFrame(data = list(zip(sido, gungu, rank, totscore, grade, score)), columns = mycolumn)
print(myframe)
print('-' * 40)

filename = 'KoreaSecurityIndex.csv'
myframe.to_csv(filename, encoding='utf8')
print(filename, ' saved...', sep='')
print('finished')