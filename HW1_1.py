import requests
from pprint import pprint
import json

#pp_key = ""

user = 'microsoft'
url = f"https://api.github.com/users/{user}"
response = requests.get(url).json()

url2 = f"https://api.github.com/users/{user}/repos"
response2 = requests.get(url2).json()

values = [element['name']
        for element in response2]



with open('data.txt', 'w') as outfile:
    json.dump(requests.get(url2).json(), outfile)

print(f'У пользователя {response.get("name")} следующий список репозиториев: {values}')

