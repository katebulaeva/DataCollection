from lxml import html
import requests
from pprint import pprint
import pymongo
from pymongo import MongoClient
from datetime import datetime as DT
from pymongo.errors import *

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

# собираем с мэйл.ру

response = requests.get('https://news.mail.ru/', headers=header)

dom = html.fromstring(response.text)

main_news = []
items = dom.xpath("//div[contains(@class,'daynews__item')]")

for item in items:
    news = {}

    title = item.xpath(".//span[contains(@class,'photo__title')]/text()")[0]
    link = item.xpath(".//@href")[0]
    id = item.xpath(".//@data-id")[0]

    news_page = requests.get(link, headers=header)
    news_dom = html.fromstring(news_page.text)
    date = news_dom.xpath("//@datetime")[0]
    description = news_dom.xpath("//div[contains(@class,'article__intro')]/p/text()")[0]
    source = news_dom.xpath("//a[contains(@class , 'breadcrumbs__link')]/span/text()")[0]


    news['title'] = title.replace('\xa0', ' ')
    news['link'] = link
    news['date'] = date[:10:]
    news['description'] = description.replace('\xa0', ' ')
    news['source'] = source
    news['news_id'] = id + "__1"


    main_news.append(news)

# собираем с лента.ру
url = 'https://lenta.ru/'
response_lenta = requests.get(url, headers=header)
dom = html.fromstring(response_lenta.text)

items_lenta = dom.xpath("//a[contains(@class,'_topnews')]")
count = 0
for item in items_lenta:
    news_lenta = {}
    count += 1
    link = item.xpath(".//@href")[0]
    # если ссылка на мослента.ру, а не лента.ру
    if link[:5:] == 'https':
        link = link
        date = link[-15:-5]
        date = DT.strptime(date, '%d-%m-%Y')
        date.strftime('%Y/%m/%d')
        id = link[-40:-16:]
        source = link[8:19:]
        news_page = requests.get(link, headers=header)
        news_dom = html.fromstring(news_page.text)
        description = news_dom.xpath("//div[contains(@class,' text ')]/p[1]/text()")[0]

    else:
        id = link.replace('/', '_')
        # открываем страницу новости и скрапим ее описание
        news_page = requests.get(url + link, headers=header)
        news_dom = html.fromstring(news_page.text)
        description = news_dom.xpath("//div[contains(@class,'topic-header__title-yandex')]/text()")
        for i in range(0, len(description)):
            description = (description[i])

        date = link.replace('/', '-')
        date = date[6:16:]
        id = link.replace('/', '_')
        source = 'lenta.ru'
        link = url + link

    title = item.xpath(".//span/text()")

    if len(title) == 0:  # у главной новости другой заголовок
        title = item.xpath(".//h3[contains(@class, 'card-big__title')]/text()")
    for i in range(0, len(title)):
        title = (title[i])

    news_lenta['title'] = title
    news_lenta['link'] = link
    news_lenta['date'] = date
    news_lenta['description'] = description
    news_lenta['source'] = source
    news_lenta['news_id'] = id[6::] + "_2"

    main_news.append(news_lenta)

# добавлям данные в базу

client = MongoClient('127.0.0.1', 27017)

db = client['user_kate']

news_db = db.news_db

news_db.create_index([('news_id', pymongo.TEXT)], name='news_index', unique=True)

count = 0
count_dupl = 0
for i in main_news:
    try:
        #news_db.insert_one(i)
        news_db.update_one({'news_id': i['news_id']}, {'$set': i}, upsert=True)
        count += 1
    except PyMongoError as e:
        print(e)
        count_dupl += 1
print(f'количество обновленных данных {count} количество ошибок {count_dupl}')





#pprint(main_news)