import scrapy
import re
import os
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


# class JobparserPipeline(object):
#     def __init__(self):
#         client = MongoClient('localhost', 27017)
#         self.mongobase = client.vacansy_280
#
#     def process_item(self, item, spider):
#         collection = self.mongobase[spider.name]
#         collection.insert_one(item)
#
#         print(item['salary_min'])
#
#         return item


class LeroyparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy_products

    def process_item(self, item, spider):
        print('start pi')
        item['_id'] = item['_id'][0]
        item['link'] = item['link'][0]
        item['price'] = item['price'][0]
        item['characteristic'] = {
            item['terms'][i]: item['definitions'][i] for i in range(len(item['terms']))
        }

        del item['terms'], item['definitions']
        collection = self.mongo_base[spider.name]
        collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)

        return item


class LeroyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                yield scrapy.Request(img)

    def file_path(self, request, response=None, info=None):
        pattern = re.compile('\/(\d+)')
        name = re.findall(pattern, request.url)[0]
        path = f'{os.getcwd()}\\images\\{name}\\'
        if os.path.exists(path) == False:
            os.mkdir(path)
        tail = os.path.basename(request.url)
        result = f'{path}{tail}'
        return result

    def item_completed(self, results, item, info):
        if results[0]:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
# class LeroymerlinparserPipeline(object):
#     def __init__(self):
#         client = MongoClient('localhost', 27017)
#         self.mongobase = client.vacansy_281
#
#     def process_item(self, item, spider):
#         collection = self.mongobase[spider.name]
#         collection.insert_one(item)
#
#         print(item['name'])
#
#         return item
#
#
# class LeroymerlinPhotosPipeline(ImagesPipeline):
#
#     def get_media_requests(self, item, info):
#         if item['photos']:
#             for img in item['photos']:
#                 try:
#                     yield scrapy.Request(f'http:{img}')
#                 except Exception as e:
#                     print(e)
#
#     def item_completed(self, results, item, info):
#         if results:
#             item['photos'] = [itm[1] for itm in results if itm[0]]
#
#         return item
