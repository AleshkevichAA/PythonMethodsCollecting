from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
import string

# vacancy - имя вакансии
# page_count - количество страниц для поиска
def _parser_hh(vacancy,page_count):
    vacancy_date = []

    params = {
        'items_on_page': '20',
        'text': vacancy,
        'clusters': 'true',
        'ored_clusters': 'true',
        'enable_snippets': 'true',
        'st': 'searchVacancy',
        'area': '1',  # Москва из справочника
        'search_field': 'name'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/92.0.1'
    }

    link = 'https://hh.ru/search/vacancy'

    html = requests.get(link, params=params, headers=headers)

    if html.ok:
        parsed_html = bs(html.text, 'html.parser')

        # на каждой страницы 20 вакансий
        # проверил для себя можно ли читать все вакансии перебором страниц до конца
        page_size = parsed_html.findAll('p', {'class': 'vacancysearch-xs-header-text'}).__getitem__(
            0).getText().replace(u'\xa0', u' ')
        # Дуболомно, но работает
        page_size = page_size.replace(" ", "")
        page_size = page_size.replace("Найдено", "")
        page_size = page_size.replace("Найдена", "")
        page_size = page_size.replace("вакансий", "")
        page_size = page_size.replace("вакансия", "")
        page_size = page_size.replace("вакансии", "")
        page_size = (int)(page_size)

        if page_size < 21:
            last_page = 1
        else:
            last_page = page_count
            # last_page = int(page_size / 20)

    for page in range(0, last_page):
        params['page'] = page
        html = requests.get(link, params=params, headers=headers)

        if html.ok:
            parsed_html = bs(html.text, 'html.parser')

            vacancy_items = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'}) \
                .find_all('div', {'class': 'vacancy-serp-item'})

            for item in vacancy_items:
                vacancy_date.append(_parser_item_hh(item))

    return vacancy_date


def _parser_item_hh(item):
    vacancy_date = {}

    # vacancy_name
    vacancy_name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()

    vacancy_date['vacancy_name'] = vacancy_name

    # # company_name
    company_name = item.find('div', {'class': 'vacancy-serp-item__meta-info'}) \
        .find('a') \
        .getText()

    vacancy_date['company_name'] = company_name

    # city  искали Москву, но ладно, проверим фильтр HH ) на релеватность ответов
    city = item.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}) \
        .getText() \
        .split(', ')[0]

    vacancy_date['city'] = city

    # metro station
    metro_station = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).findChild()

    if not metro_station:
        metro_station = None
    else:
        metro_station = metro_station.getText()

    vacancy_date['metro_station'] = metro_station


    # salary
    salary=None
    if (item.find('div', {'class': 'vacancy-serp-item__sidebar'}) != None):
        salary = item.find('div', {'class': 'vacancy-serp-item__sidebar'}).find('span')
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText().replace(u'\xa0', u'')

        # для борьбы с неразрывным пробелом

        salary = re.split(r'\s|-', salary)

        if salary[0] == 'до':
            salary_min = None
            if len(salary) == 4:
                salary_max = int(salary[1]) * 1000 + int(salary[2])
                salary_currency = salary[3]
            else:
                salary_max = int(salary[1])
                salary_currency = salary[2]
        elif salary[0] == 'от':
            if len(salary) == 4:
                salary_min = int(salary[1]) * 1000 + int(salary[2])
                salary_max = None
                salary_currency = salary[3]
            else:
                salary_min = int(salary[1])
                salary_max = None
                salary_currency = salary[2]
        else:
            if (len(salary) == 6):
                salary_min = int(salary[0]) * 1000 + int(salary[1])
                salary_max = int(salary[3]) * 1000 + int(salary[4])
                salary_currency = salary[5]
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[1])
                salary_currency = salary[2]

    vacancy_date['salary_min'] = salary_min
    vacancy_date['salary_max'] = salary_max
    vacancy_date['salary_currency'] = salary_currency

    # link
    # is_ad = item.find('span', {'class': 'vacancy-serp-item__controls-item vacancy-serp-item__controls-item_last'}) \
    #     .getText()

    vacancy_link = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

    # if is_ad != 'Реклама':
    #     vacancy_link = vacancy_link.split('?')[0]

    vacancy_date['vacancy_link'] = vacancy_link

    # site
    vacancy_date['site'] = 'hh.ru'

    return vacancy_date


def _parser_superjob(vacancy,count_page):
    vacancy_date = []

    params = {
        'keywords': vacancy, \
        'profession_only': '1', \
        'geo[c][0]': '15', \
        'geo[c][1]': '1', \
        'geo[c][2]': '9', \
        'page': ''
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }

    link = 'https://www.superjob.ru/vacancy/search/'

    html = requests.get(link, params=params, headers=headers)

    if html.ok:
        parsed_html = bs(html.text, 'html.parser')

        page_block = parsed_html.find('a', {'class': 'f-test-button-1'})
    if not page_block:
        last_page = 1
    else:
        # page_block = page_block.findParent()
        # last_page = int(page_block.find_all('a')[-2].getText())
        last_page=int(count_page)
    for page in range(0, last_page + 1):
        params['page'] = page
        html = requests.get(link, params=params, headers=headers)

        if html.ok:
            parsed_html = bs(html.text, 'html.parser')
            vacancy_items = parsed_html.find_all('div', {'class': 'f-test-vacancy-item'})

            for item in vacancy_items:
                vacancy_date.append(_parser_item_superjob(item))

    return vacancy_date


def _parser_item_superjob(item):
    vacancy_date = {}

    # vacancy_name
    vacancy_name = item.find_all('a')[0].getText()
    # if len(vacancy_name) > 1:
    #     vacancy_name = vacancy_name[0].getText()
    # else:
    #     vacancy_name = vacancy_name[0].getText()
    vacancy_date['vacancy_name'] = vacancy_name

    # company_name
    company_name = item.find('span', {'class': 'f-test-text-vacancy-item-company-name'}).find('a').getText()

    # if not company_name:
    #     company_name = item.findParent() \
    #         .find('span', {'class': 'f-test-text-vacancy-item-company-name'}) \
    #         .getText()
    # else:
    #     company_name = company_name.getText()

    vacancy_date['company_name'] = company_name

    # city
    # company_location = item.find('span', {'class': 'f-test-text-company-item-location'}) \
    #     .findChildren()[1] \
    #     .getText() \
    #     .split(',')
    company_location = item.find('span', {'class': 'f-test-text-company-item-location'}).findAll('span')[2].getText()
    vacancy_date['city'] = company_location

    # metro station
    # if len(company_location) > 1:
    #     metro_station = company_location[1]
    # else:
    #     metro_station = None
    #
    # vacancy_date['metro_station'] = metro_station

    # salary
    # salary = item.find('span', {'class': 'f-test-text-company-item-salary'}) \
    #     .findChildren()
    salary = item.find('span', {'class': 'f-test-text-company-item-salary'}).findChildren()[0]
    if not salary or salary.getText()=='По договорённости':
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText()
            # .replace(u'\xa0', u'')
        # salary = salary.replace('<!-- -->',u'')
        # для борьбы с неразрывным пробелом

        salary = re.split(r'\s|-', salary)

        if salary[0] == 'до':
            salary_min = None
            if len(salary) == 4:
                salary_max = int(salary[1]) * 1000 + int(salary[2])
                salary_currency = salary[3]
            else:
                salary_max = int(salary[1])
                salary_currency = salary[2]
        elif salary[0] == 'от':
            if len(salary) == 4:
                salary_min = int(salary[1]) * 1000 + int(salary[2])
                salary_max = None
                salary_currency = salary[3]
            else:
                salary_min = int(salary[1])
                salary_max = None
                salary_currency = salary[2]
        else:
            if (len(salary) == 6):
                salary_min = int(salary[0]) * 1000 + int(salary[1])
                salary_max = int(salary[3]) * 1000 + int(salary[4])
                salary_currency = salary[5]
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[1])
                salary_currency = salary[2]

    vacancy_date['salary_min'] = salary_min
    vacancy_date['salary_max'] = salary_max
    vacancy_date['salary_currency'] = salary_currency

    # link
    vacancy_link = item.find_all('a')

    # if len(vacancy_link) > 1:
    #     vacancy_link = vacancy_link[-2]['href']
    # else:
    #     vacancy_link = vacancy_link[0]['href']
    vacancy_link = vacancy_link[0]['href']
    vacancy_date['vacancy_link'] = f'https://www.superjob.ru{vacancy_link}'

    # site
    vacancy_date['site'] = 'www.superjob.ru'

    return vacancy_date

# основной метод
def parser_vacancy(vacancy,count_page):
    vacancy_date = []
    vacancy_date.extend(_parser_hh(vacancy,count_page))
    print(f'Параметры запуска:{vacancy},{count_page} стр. Распарсили {len(vacancy_date)} вакансий с hh.ru')
    vacancy_date.extend(_parser_superjob(vacancy,count_page))
    print(f'Параметры запуска:{vacancy},{count_page} стр. Распарсили {len(vacancy_date)} вакансий с superjob.ru')

    df = pd.DataFrame(vacancy_date)

    return df

## Поищем по 2 страницы Java разработчика
vacancy = 'Java developer'
count_page = 10
df = parser_vacancy(vacancy,count_page)
print(f'Зарплата в валюте отличной от руб, конечно даст искажения статистических данных')
print(df.describe())
