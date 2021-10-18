import scrapy
from scrapy.http import HtmlResponse
import re
from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']

    def __init__(self, vacancy=None):
        super(SuperjobruSpider, self).__init__()
        self.start_urls = [
            f'https://www.superjob.ru/vacancy/search/?keywords={vacancy}&geo[t][0]=4'

        ]

    def parse(self, response: HtmlResponse):

        next_page = 'https://superjob.ru' + response.css('a[rel="next"]::attr(href)').extract_first()

        yield response.follow(next_page, callback=self.parse)

        # vacancy_items = response.css('div[class="f-test-vacancy-item"]::attr(href)').extract()
        vacancy_items = response.css(
            'div.f-test-vacancy-item \
            a[class*=f-test-link][href^="/vakansii"]::attr(href)'
        ).extract()
        # распарсим вакансии по ссылке
        for vacancy_link in vacancy_items:
            yield response.follow('https://superjob.ru' + vacancy_link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1 ::text').extract()

        # # company_name
        company_name = response.css('span[class*=f-test-text-vacancy-item-company-name] a::text').extract_first()

        city = response.css('span[class*=f-test-text-company-item-location] span span::text').extract_first()

        metro_station = response.css('div[class*=f-test-address] span::text').extract_first()
        salary_min=None
        salary_max=None
        salary_currency=None
        # salary=''.join(response.css('span[data-qa="vacancy-serp__vacancy-compensation"]::text').getall())

        if len(response.css('span[class*="f-test-text-company-item-salary"] span span').extract()) > 0:
            salary = \
            response.css('span[class*="f-test-text-company-item-salary"] span span').extract()[0].split('">')[1].split('</sp')[0].replace('<!-- -->','')
            # по договоренности
            if ((salary[0] == 'По') | (salary == 'По договорённости')):
                salary = None
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
                elif (len(salary) == 2):
                    salary_min = int(salary[0]) * 1000 + int(salary[1])
                    # salary_max = int(salary[0]) * 1000 + int(salary[1])
                    salary_currency = 'руб'
                elif (len(salary) == 3):
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
