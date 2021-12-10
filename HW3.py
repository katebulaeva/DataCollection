from pprint import pprint
from HW2 import vacancy_list
import pymongo
from pymongo import MongoClient
from pymongo.errors import *

client = MongoClient('127.0.0.1', 27017)

db = client['user_kate']

vacancies = db.vacancies
#vacancies.insert_one(vacancy_list[0])
vacancies.create_index([('vac_id', pymongo.TEXT)], name='link_index', unique=True)

count = 0
count_dupl = 0
for i in vacancy_list:
    try:
        vacancies.insert_one(i)
        count += 1
    except DuplicateKeyError as e:
        count_dupl += 1
print(f'количество новых данных {count} количество дубликатов {count_dupl}')



#Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты)
input = int(input ("Введите желаемую зп: "))
for doc in vacancies.find({'$or': [{'min_salary': {'$gte':input}}, {'max_salary': {'$gte':input}}]}):
     pprint(doc)




print(1)