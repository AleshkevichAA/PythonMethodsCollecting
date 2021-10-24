import scrapy
import re
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    company_name = scrapy.Field()
    city = scrapy.Field()
    metro_station = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_currency = scrapy.Field()
    vacancy_link = scrapy.Field()
    site = scrapy.Field()




# class LeroymerlinItem(scrapy.Item):
#     # define the fields for your item here like:
#     _id = scrapy.Field()
#     name = scrapy.Field()
#     photos = scrapy.Field()
#     price = scrapy.Field()
#     pass


import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def cleaner_url(url):
    if url[:2] == '//':
        return f'https:{url}'
    return url


def parse_params(params):
    params = [i.strip().strip(':').replace('\xa0', ' ') for i in params]
    result = dict(zip(params[1::3], params[2::3]))
    return result


def get_id(values):
    pattern = re.compile('(\d+)\/')
    values = int(re.findall(pattern, values)[0])
    return values


def get_link(values):
    pattern = re.compile('<\d+ (.+)>')
    values = re.findall(pattern, values)
    return values


def edit_definitions(values):
    pattern = re.compile('\\n +')
    values = re.sub(pattern, '', values)
    try:
        return float(values)
    except ValueError:
        return values


def change_price(values):
    values = float(values)
    return values


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field(input_processor=MapCompose(get_id))
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose())
    terms = scrapy.Field(input_processor=MapCompose())
    definitions = scrapy.Field(input_processor=MapCompose(edit_definitions))
    price = scrapy.Field(input_processor=MapCompose(change_price))
    characteristic = scrapy.Field()
    link = scrapy.Field(output_processor=MapCompose(get_link))
