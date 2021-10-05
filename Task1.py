#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
#сохранить JSON-вывод в файле *.json.
import requests
import json

url = 'https://api.github.com'
user='AleshkevichAA'

r = requests.get(f'{url}/users/{user}/repos')

with open('data.json', 'w') as f:
    json.dump(r.json(), f)

print(r.json())

print('REPO LIST:')
print('name:full_name')
for i in r.json():
    print(i['name'] +':'+i['full_name'])





