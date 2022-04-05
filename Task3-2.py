# Парсинг HTML. BS, SQLAlchemy
# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from ScrapingJob3 import ScrapingJob3
from pprint import pprint

# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
# vacancy - имя вакансии
# count_page - количество страниц в поиске
def scrap(vacancy,count_page):
    vacancy_db = ScrapingJob3('mongodb://localhost:27017/', 'vacancy', 'vacancy_db')
    # vacancy = 'Java developer'
    # vacancy = 'Генетик'
    # count_page = 2
    df =vacancy_db.search_job(vacancy, count_page)
    print(df.describe())
    return vacancy_db


vacancy_db=scrap('Python',10)
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
def findSalary(vacancy_db):
    salary=int(input('Введите искомую зарплату(например, 50000):'))
    vacancy_db.print_salary(salary)

findSalary(vacancy_db)

# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
# при добавлении используем функцию, чтобы понять, надо ли обновить, или добавить новую сущность
#vacancy_db.is_exists()

# dj
# objects = vacancy_db.collection.find().limit(1)
# for obj in objects:
#     pprint(obj)

