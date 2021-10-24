# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import re
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']

    def __init__(self, vacancy=None):
        super(HhruSpider, self).__init__()
        self.start_urls = [
            f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text={vacancy}'
        ]

    def parse(self, response: HtmlResponse):

        next_page = 'https://hh.ru' + response.css('a[data-qa="pager-next"]::attr(href)').extract_first()

        yield response.follow(next_page, callback=self.parse)

        vacancy_items = response.css('a[data-qa="vacancy-serp__vacancy-title"]::attr(href)').extract()

        # распарсим вакансии по ссылке
        for vacancy_link in vacancy_items:
            yield response.follow(vacancy_link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('a[data-qa="vacancy-serp__vacancy-title"]::text').extract_first()

        # # company_name
        company_name = response.css('a[data-qa="vacancy-serp__vacancy-employer"]::text').extract_first()

        city = response.css('a[data-qa="vacancy - serp__vacancy - address"]::text').extract_first()
        # city="Москва"

        metro_station = response.css('span[class="metro-station"]::text').extract_first()

        # salary=''.join(response.css('span[data-qa="vacancy-serp__vacancy-compensation"]::text').getall())
        if len(response.css('span[data-qa="vacancy-serp__vacancy-compensation"]::text').getall()) > 1:
            salary = response.css('span[data-qa="vacancy-serp__vacancy-compensation"]::text').getall()[0] + \
                     response.css('span[data-qa="vacancy-serp__vacancy-compensation"]::text').getall()[1]
        else:
            salary = None
        if (salary is None):
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
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
                elif (len(salary) == 5):
                    salary_min = int(salary[0])
                    salary_max = int(salary[2]) * 1000 + int(salary[3])
                    salary_currency = salary[4]
                else:
                    salary_min = int(salary[0])
                    salary_max = int(salary[1])
                    salary_currency = salary[2]

        print(
            f'\nНазвание вакансии:{name} ({company_name},{metro_station}), {salary_min}-{salary_max} {salary_currency} ')

        vacancy_link = response.url
        site = self.allowed_domains[0]

        yield JobparserItem(name=name, company_name=company_name, city=city, metro_station=metro_station,
                            salary_min=salary_min,
                            salary_max=salary_max, salary_currency=salary_currency, vacancy_link=vacancy_link,
                            site=site)
