from jobparser.spiders.hhru import HhruSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.superjobru import SuperjobruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    vacancy='Java'
    process.crawl(HhruSpider, vacancy=vacancy)
    process.crawl(SuperjobruSpider, vacancy=vacancy)
    process.start()
