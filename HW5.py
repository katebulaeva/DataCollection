from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pprint import pprint
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pymongo
from pymongo import MongoClient
from pymongo.errors import *



driver = webdriver.Chrome("./chromedriver.exe")

list_mails = []


driver.get("https://mail.ru")
# вводим логин
element = driver.find_element(By.NAME, "login")
element.send_keys("study.ai_172")

element.send_keys(Keys.ENTER)
time.sleep(1)
# вводим пароль
element = driver.find_element(By.NAME, "password")
element.send_keys("NextPassword172#")
element.send_keys(Keys.ENTER)

# ждем пока прогрузятся письма (кстати не сразу поняла, на что же выводит ошибку в wait.until, оказалось там нужны двойные скобки !!!
wait = WebDriverWait(driver, 10)
button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal')]")))
main_window = driver.current_window_handle
# собираем элементы, скроллим вниз, снова собираем элементы (вопрос, а как смотреть код элемента, если нажатие правой кнопки дает меню сайта? (нашла, с помощью пробела))
for i in range(2): # для проверки работоспособности, 2х страниц достаточно

    mails = driver.find_elements(By.XPATH, "//a[contains(@class, 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal')]")


    for mail in mails: #[:5:]: #использовала для быстрого тестирования
        mail_data = {}
        #id = driver.__getattribute__((By.XPATH, '//@data-uidl-id')) #не получается
        #link = mail.get_attribute((By.XPATH, "//@href")) #не получается :(
        ActionChains(driver) \
            .key_down(Keys.LEFT_CONTROL) \
            .click(mail) \
            .key_up(Keys.LEFT_CONTROL) \
            .perform()
        #href = mail.click()
        driver.switch_to.window(driver.window_handles[1])
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__body')))
        #wait = WebDriverWait(driver, 10)
        #time.sleep(5)

        sent_from = driver.find_element(By.CLASS_NAME, "letter-contact").text
        sent_date = driver.find_element(By.CLASS_NAME, "letter__date").text
        # начинается с "сегодня"
        if sent_date[:5:] == 'Сегод':
            sent_date = date.today().strftime('%d %B %Y') + ' ' + sent_date[-5::]
            elif
        #id = sent_date.replace(' ','').replace(',', '') + sent_from.replace('@','')
        id = sent_date.replace(' ','').replace(',', '').replace(':','') + sent_from.replace('@','').replace('.','')


        mail_head = driver.find_element(By.XPATH, "//h2[contains(@class, 'thread-subject')]").text
        mail_texts = driver.find_elements(By.XPATH, "//table")
        text = ''
        for i in mail_texts:

            text1 = i.text
            text = text + '\n' + text1
            wait = WebDriverWait(driver, 10)
        #pprint(text)
        mail_data['sent_from'] = sent_from
        mail_data['sent_date'] = sent_date
        mail_data['mail_head'] = mail_head
        mail_data['mail_texts'] = text
        mail_data['mail_id'] = id


        #wait = WebDriverWait(driver, 10)

        driver.close()
        time.sleep(1)
        list_mails.append(mail_data)
        driver.switch_to.window(main_window)


    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

    time.sleep(2)

pprint(list_mails)

#driver.quit()


# добавлям данные в базу

client = MongoClient('127.0.0.1', 27017)

db = client['user_kate']

mails_db = db.mails_db

mails_db.create_index([('mail_id', pymongo.TEXT)], name='mail_index', unique=True)


count = 0
count_dupl = 0
for i in list_mails:
    try:
        #news_db.insert_one(i)
        mails_db.update_one({'mail_id': i['mail_id']}, {'$set': i}, upsert=True)
        count += 1
    except PyMongoError as e:
        print(e)
        count_dupl += 1
print(f'количество обновленных данных {count} количество ошибок {count_dupl}')

