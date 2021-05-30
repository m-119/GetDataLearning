import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

driver = webdriver.Chrome()
driver.get('https://www.mvideo.ru')

xpath_nxt = "//h2[contains(text(), 'Новинки')]/ancestor::div[@class= 'section']/descendant::a[contains(@class,'next-btn')]"
xpath_itm = "//h2[contains(text(), 'Новинки')]/ancestor::div[@class= 'section']/descendant::li[@class='gallery-list-item']"
xpath_scr = "//h2[contains(text(), 'Новинки')]/ancestor::div[@class= 'section']/descendant::li[@class='gallery-list-item']/div/script"

el = WebDriverWait(driver, 5)

while True:
    driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
    sleep(.05)
    try:
        driver.find_element_by_xpath(xpath_nxt)
    except:
        continue
    break

el.until(EC.element_to_be_clickable((By.XPATH, xpath_itm)))

ccnt = 0
ecnt = len(driver.find_elements_by_xpath(xpath_itm))

while ccnt != ecnt:
    ccnt = ecnt
    driver.find_element_by_xpath(xpath_nxt).click()
    el.until(EC.element_to_be_clickable((By.XPATH, xpath_itm)))
    while True:
        sleep(2)
        t = None
        try:
            t = driver.find_elements_by_css_selector('.ajax-overlay_show')
        except:
            pass
        if not t:
            break
    ecnt = len(driver.find_elements_by_xpath(xpath_itm))
    #print(ccnt, ecnt)

### запись в БД ###
client = MongoClient('127.0.0.1', 27017)

db: Database = client['newMvideo']

newMvideo: Collection = db.newMvideo

result = []
for e in driver.find_elements_by_xpath(xpath_scr):
    pass
    j = e.get_attribute('innerHTML')
    #print(json.loads(j.split("[")[3].split("]")[0].replace(r'\n','').replace('\'','"')))
    newMvideo.insert_one(j)