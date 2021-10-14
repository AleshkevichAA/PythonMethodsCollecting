# Lesson 04
#
# Парсинг HTML. XPath
#
# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
#
#     название источника;
#     наименование новости;
#     ссылку на новость;
#     дата публикации.


from lxml import html
import requests
import pprint
from datetime import datetime


def get_news_lenta_ru():
    news = []

    keys = ('title', 'date', 'link')
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    link_lenta = 'https://lenta.ru/'

    request = requests.get(link_lenta)

    root = html.fromstring(request.text)
    root.make_links_absolute(link_lenta)

    news_links = root.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/@href''')

    news_text = root.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/text()''')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_date = []

    for item in news_links:
        request = requests.get(item)
        root = html.fromstring(request.text)
        date = root.xpath('//time[@itemprop="datePublished"]/@datetime')
        news_date.extend(date)

    for i in range(len(news_date)):
        news_date[i] = datetime.strptime(news_date[i], date_format)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'lenta.ru'
        news.append(news_dict)

    return news


def get_news_mail_ru():
    news = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }

    keys = ('title', 'date', 'link')
    date_format = '%Y-%m-%dT%H:%M:%S%z'

    link_mail_ru = 'https://mail.ru/'

    request = requests.get(link_mail_ru, headers=headers)
    root = html.fromstring(request.text)

    news_links = root.xpath('''(//div[@class =  "news-item o-media news-item_media news-item_main"]  |  
                                //div[@class =  "news-item__inner"])
                                /a[contains(@href, "news.mail.ru")]/@href''')

    news_text = root.xpath('''(//div[@class =  "news-item o-media news-item_media news-item_main"]//h3  |  
                               //div[@class =  "news-item__inner"]/a[contains(@href, "news.mail.ru")])
                               /text()''')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_links_temp = []
    for item in news_links:
        item = item.split('/')
        news_links_temp.append('/'.join(item[0:5]))

    news_links = news_links_temp
    del (news_links_temp)

    news_date = []

    for item in news_links:
        request = requests.get(item, headers=headers)
        root = html.fromstring(request.text)
        date = root.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')
        news_date.extend(date)

    for i in range(len(news_date)):
        news_date[i] = datetime.strptime(news_date[i], date_format)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'mail.ru'
        news.append(news_dict)

    return news

# get_news_lenta_ru()

# from pprint import pprint
# from lxml import html
# import requests
# import time
# header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
# def request_to_yandex(str):
#     try:
#         time.sleep(1)
#         response = requests.get('https://yandex.ru/search/',params={'text':str},headers = header)
#         root = html.fromstring(response.text)
#         result = root.xpath("//a[contains(@class,'link_cropped_no')]/@href |a[contains(@class,'organic__url_type_multiline')]/@href")
#         return result
#     except:
#         print('Ошибка запроса')
# for i in range(50):
#    result = request_to_yandex('Шляпа')
# pprint(result)

def get_news_kolesa_ru():
    news = []

    keys = ('title', 'date', 'link')

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/92.0.1'
    }

    link_kolesa = 'https://kolesa.ru/'

    request = requests.get(link_kolesa,headers=headers)

    root = html.fromstring(request.text)
    root.make_links_absolute(link_kolesa)

    # получим линки на актуальные новости на главной странице
    news_links = root.xpath("(//a[@class='promo-block-item large tile'])/@href")
    news_link_smalls= root.xpath("(//a[@class='promo-block-item tile'])/@href")
    news_links=news_links+news_link_smalls
    # print(news_links)

    # тут почему-то первый пустой
    news_text=root.xpath("//span[@class='tile-title']/text()")
    del news_text[0]

    news_time=root.xpath("//a[@class='promo-block-item large tile']/span[@class='tile-title']/time/text()")
    news_date = []

    for item in news_links:
        news_date.extend(news_time)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = link_kolesa
        news.append(news_dict)

    return news

def get_news_autoreview_ru():
    news = []

    keys = ('title', 'date', 'link')

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/92.0.1'
    }

    link_autoreview = 'https://autoreview.ru/'

    request = requests.get(link_autoreview,headers=headers)

    root = html.fromstring(request.text)
    root.make_links_absolute(link_autoreview)

    # получим линки на актуальные новости на главной странице
    news_links = root.xpath("(//div[@class='item'])/@data-href")
    print(news_links)

    # название новости
    news_text= root.xpath("(//div[@class='item'])/a[@class='link']/text()")


    news_date=root.xpath("(//div[@class='item'])/div[@class='date']/text()")

    for i in range(len(news_date)):
        news_date[i]=news_date[i].rstrip()
        if ((len(news_date[i])==0) | ("АР" in news_date[i])):
            news_date[i]='Нет даты'

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = link_autoreview
        news.append(news_dict)
    return news

def get_news_mag_auto_ru():
    news = []

    keys = ('title', 'date', 'link')

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/92.0.1'
    }

    link_mag_auto = 'https://mag.auto.ru/theme/news/'

    request = requests.get(link_mag_auto,headers=headers)

    root = html.fromstring(request.text,'Koi-8r')
    root.make_links_absolute(link_mag_auto)

    # получим линки на актуальные новости на главной странице
    news_links = root.xpath("(//a[@class='MagLink MagLink_color_black'])/@href")
    print(news_links)

    # название новости
    news_text= root.xpath("(//a[@class='MagLink MagLink_color_black'])/text()")
    # for i in range(len(news_text)):
    #     news_text[i]=


    news_date=root.xpath("(//div[@class='BlockTypePost__descriptionMeta'])/time/@datetime")

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = link_mag_auto
        news.append(news_dict)
    return news


print(f'Новости kolesa.ru {get_news_kolesa_ru()}')
print(f'Новости autoreview.ru {get_news_autoreview_ru()}')
print(f'Новости mag.auto.ru {get_news_mag_auto_ru()}')