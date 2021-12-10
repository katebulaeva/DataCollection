import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd


url = 'https://www.hh.ru'

search = 'data scientist'

# https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text=data+scientist&from=suggest_post
# https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&clusters=true&ored_clusters=true&enable_snippets=true&text=data+scientist&from=suggest_post


params = {'clusters': 'true',
          'area': 1,
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'salary': '&',
          'text': search,
          'from': 'suggest_post',
          'page': 1,
          'items_on_page': 10}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

last_page = int(dom.find('span', {'class', 'bloko-form-spacer'}).nextSibling.nextSibling.nextSibling.text)
vacancy_list = []

for i in range(1, last_page):
    params['page'] = i
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})


    for vacancy in vacancies:
        vacancy_data = {}
        name = vacancy.find('a')
        link = name.get('href')
        name = name.text
        employer = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text.replace('\xa0', ' ')
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        try:
            salary = salary.text.replace('\u202f', '')

            salary1 = []
            max_salary = []
            min_salary = []
            currency = []
            salary1 = salary.split(' ')

            if salary1[0] == 'от':
                min_salary.append(int(salary1[1]))
                min_salary = int(' '.join(map(str, min_salary)))
                currency.append(salary1[2])
                currency = ' '.join(map(str, currency))
                max_salary = None

            elif salary1[1] == '–':

                max_salary.append(int(salary1[2]))
                max_salary = int(' '.join(map(str, max_salary)))
                min_salary.append(int(salary1[0]))
                min_salary = int(' '.join(map(str, min_salary)))
                currency.append(salary1[3])
                currency = ' '.join(map(str, currency))

            elif salary1[0] == 'до':
                max_salary.append(int(salary1[1]))
                max_salary = int(' '.join(map(str, min_salary)))
                currency.append(salary1[2])
                currency = ' '.join(map(str, currency))

        except:
            salary = None
            min_salary = None
            max_salary = None
            currency = None

        vacancy_data['name'] = name
        vacancy_data['employer'] = employer
        #vacancy_data['salary'] = salary
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        vacancy_data['currency'] = currency
        vacancy_data['link'] = link
        vacancy_data['vac_id'] = link[22:30]

        vacancy_list.append(vacancy_data)

#pprint(vacancy_list)

df = pd.DataFrame()
for i in vacancy_list:
    dict_new = dict(i)
    df = df.append(dict_new, ignore_index=True)
#print(df)
df.to_csv('scraping_hh.csv', sep='\t', encoding='utf8')