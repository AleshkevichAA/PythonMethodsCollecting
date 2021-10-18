import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name=scrapy.Field()
    company_name = scrapy.Field()
    city = scrapy.Field()
    metro_station= scrapy.Field()
    salary_min=scrapy.Field()
    salary_max=scrapy.Field()
    salary_currency=scrapy.Field()
    vacancy_link=scrapy.Field()
    site=scrapy.Field()

