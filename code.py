import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
import csv
from html import unescape


options = Options()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"# it locates chrome app
driver=webdriver.Chrome(options=options,executable_path='C:\\Users\\<username>\\Downloads\\chromedriver_win32\\chromedriver')#IT LOCATES chromedriver
driver.implicitly_wait(10)
url='https://propane.com/where-to-buy/'
driver.get(url)
time.sleep(3)

value=input("Enter any of them(8000/16000/32000/80000/160000) for 5miles/10miles/20/miles/50miles/100miles: ")
# driver.find_element_by_xpath('//*[@id="cookie-consent"]/div/div/button/span').click()
driver.find_element(By.XPATH, '//*[@id="cookie-consent"]/div/div/button/span').click()
time.sleep(1)

searchBox=driver.find_element(By.XPATH, '//*[@id="locator-map-supplier"]/section/div/form/div/input')
searchBox.send_keys('10001')
time.sleep(1)

dropdown=driver.find_element(By.XPATH, '//option[@value='+value+']').click()
time.sleep(1)

searchBtn=driver.find_element(By.XPATH, '//*[@id="locator-map-supplier"]/section/div/form/div/button/span').click()

info_xpath='//*[@class="map__result"]/*'
last_element_infopath='//*[@class="map__result map__result--current"]'
time.sleep(3)

while True:

    try:
          load_more_element=driver.find_element(By.XPATH, '//*[@id="locator-map-supplier"]/section/div/div/div/div/ul/li/button/span')
          load_more_element.click()
    except exceptions.StaleElementReferenceException:  
        break
    except exceptions.NoSuchElementException:
        break
        
time.sleep(3)
li=driver.find_elements_by_link_text('View Contact Info')
for i in li:
    i.click()
    time.sleep(1.6)
info_li=driver.find_elements_by_xpath(info_xpath)
last_info=driver.find_elements_by_xpath(last_element_infopath)

fields=["Company","Address","Contact No","Opening Times","Website"]
with open("E:\\Projects\\propane_crawling.csv","w",newline="") as f:
    writer=csv.DictWriter(f,delimiter="\n",fieldnames=fields)
    writer.writeheader()
    string=""
   
    for i in info_li:
        s=str(i.text)
        string += "\n"+s
    for j in last_info:
        s=str(j.text)
        string += "\n"+s

li_text=string.split("View on Map")
if li_text[-1]=="":
    li_text.pop()
with open("propane_crawling.csv","w",newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,['Distance','Company','Location','Contact','Time','Website'])
    writer.writeheader()
    for i in li_text:
        final_li=(i.split("\n"))
        for _ in final_li:
            if _=="":
                final_li.remove("")
    
        length_final=len(final_li)
        distance=final_li[0]
        company=final_li[1]
        location=final_li[2]
        contact="Not existed"
        website="Not existed"
        time="Not existed"
        if final_li[3][-3:] != "com":
            contact=final_li[3]
        if final_li[-1][-3:]=="com":
            website=final_li[-1]
         
        if length_final==6:
            time=final_li[4]
        
        elif final_li[-1][-3:] != "com" and length_final==5:
            time=final_li[-1]
        
        writer.writerow({'Distance':distance,'Company':company,'Location':location,'Contact':(contact),'Time':time,'Website':website})
        

driver.quit()
