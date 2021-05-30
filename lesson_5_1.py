from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



driver = webdriver.Chrome()

params = {
    'link': 'https://account.mail.ru/login',
    'login': 'study.ai_172@mail.ru',
    'pwd': 'NextPassword172!'
}

driver.get(params.get('link'))

el = WebDriverWait(driver, 5)
el.until(EC.element_to_be_clickable((By.NAME, 'username')))
driver.find_element_by_name('username').send_keys(params.get('login'))
driver.find_element_by_xpath("//*[contains(text(),'Ввести пароль')]/ancestor::button").click()


el.until(EC.element_to_be_clickable((By.NAME, 'password')))
driver.find_element_by_name('password').send_keys(params.get('pwd'))
driver.find_element_by_xpath("//*[contains(text(),'Войти')]/ancestor::button").click()

# список селекторов, на основе JS (можно проверить через консоль почти любого браузера)
# document.querySelectorAll('span[class*="button2_ico-arrow-down"]') - папки с подпапками
# document.querySelectorAll('a.nav__item') - список папок
# document.querySelectorAll('a.js-letter-list-item') - список писем
#                                       письма подгружаются динамически, т.е. размер списка будет актуален только
#                                       перед окончанием прокрутки, браузеру при прокрутке не свойственно "выгружать"
#                                       элементы, поэтому есть 3 варианта сбора писем:
#                                                                       1) собирать и подгружать параллельно
#                                                                       2) загрузить весь список, после начать сбор
#                                                                       3) зайти в первое письмо и переключаться к
#                                                                       следующему, пока есть такая возможность
# document.querySelectorAll('.letter__author > .letter-contact') - от кого
# document.querySelector('.letter__date') - дата отправки
# document.querySelectorAll('.thread__subject') - тема письма
# document.querySelectorAll('.letter-body__body-content') - текст письма полный

driver.find_elements_by_css_selector('a.js-letter-list-item')
pass

menu: list = []
elms: list = []

# из вариантов сверху выбрал первый, т.к. список писем может быть очень большим

# Отобразить все подпапки
while driver.find_elements_by_css_selector('span[class*="button2_ico-arrow-down"]'):
    for e in driver.find_elements_by_css_selector('span[class*="button2_ico-arrow-down"]'):
        e.click()

result: list = []
el.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav__item')))
# получить список пунктов меню
menu = driver.find_elements_by_css_selector('a.nav__item')
elms = None
for f in menu:
    letter: dict = {'folder': f.text, 'from': None, 'date': None, 'subject': None, 'body': None}
    f.click()
    while driver.find_element_by_css_selector('.progress__value').get_attribute('style') != 'width: 100%;':
        pass
    try:
        item = driver.find_element_by_css_selector('a.js-letter-list-item')
    except:
        item = None
    # черновики?
    if f.text == 'Черновики':
        # черновики - не рассматриваются
        continue
    while True:
        # в папке есть письма
        if item:
            try:
                item.click()
            except Exception as e:
                break
            # ожидание загрузки тела письма
            while True:
                try:
                    el.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.letter__author > .letter-contact')))
                    letter['from'] = driver.find_element_by_css_selector('.letter__author > .letter-contact').text
                    break
                except Exception as e:
                    pass
                    #print(e)
                    continue
            while True:
                try:
                    el.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.letter__date')))
                    letter['date'] = driver.find_element_by_css_selector('.letter__date').text
                    break
                except Exception as e:
                    pass
                    #print(e)
                    continue
            while True:
                try:
                    el.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.thread__subject')))
                    letter['subject'] = driver.find_element_by_css_selector('.thread__subject').text
                    break
                except Exception as e:
                    pass
                    #print(e)
                    continue
            while True:
                try:
                    el.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.letter-body__body-content')))
                    letter['body'] = driver.find_element_by_css_selector('.letter-body__body-content').text
                    break
                except Exception as e:
                    pass
                    #print(e)
                    continue
            #print("-----------------------------")
        # папка пуста?
        else:
            break
        result.append(letter)
        # кнопка далее
        try:
            item = driver.find_element_by_css_selector('span[data-title-shortcut="Ctrl+↓"]')
            item.click()
        except:
            item = None
            break
        el.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.progress__value')))


#
#
#
#

#print(result)

pass

