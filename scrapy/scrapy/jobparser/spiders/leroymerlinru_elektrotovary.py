import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from jobparser.items import LeroyparserItem

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    i = 0

    def __init__(self, mark):
        self.start_urls = [f'https://leroymerlin.ru/catalogue/elektrotovary/?q={mark}']

    def __init__(self):
        self.start_urls = [f'https://leroymerlin.ru/catalogue/elektrotovary/?page=']

    def parse(self, response: HtmlResponse):
        self.i=self.i+1
        next_page = 'https://leroymerlin.ru/catalogue/elektrotovary/?page=' + (str)(self.i)
        yield response.follow(next_page, callback=self.parse)

        goods_links = response.xpath('//div[@data-qa-product=""]/a''//@href').extract()
        for link in goods_links:
            # yield response.follow('https://leroymerlin.ru' + link, callback=self.parse_ads)
            yield response.follow('https://leroymerlin.ru' + link, callback=self.parse_product)

    def parse_ads(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').extract_first()
        photos = response.xpath('//source[@media=" only screen and (min-width: 1024px)"]/@srcset').extract()
# photos = response.xpath('//source[@media=" only screen and (min-width: 1024px)" contains(@class , "gallery-img-wrapper")]'
#                                 '//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        price = float(response.xpath('//div//@data-product-price').extract_first())

        print(name[0])
        print(photos)

        yield LeroymerlinItem(name=name, photos=photos, price=price)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)

        loader.add_value('_id', str(response))
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('terms', "//dt/text()")
        loader.add_xpath('definitions', "//dd/text()")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_value('link', str(response))

        yield loader.load_item()