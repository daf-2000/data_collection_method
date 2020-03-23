import requests
import re
from pprint import pprint
from lxml import html
from datetime import datetime
from pymongo import MongoClient
header_moz = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
main_link_mail = 'https://mail.ru/'
main_link_lenta = 'https://lenta.ru/'
main_link_ya = 'https://yandex.ru/news/'
block_url_mail = "//div[@class='ssr-main']//a"
block_url_lenta = "//div[@class='b-yellow-box__wrap']//div//a"
block_url_ya = "//div[@class='rubber__col rubber__col_left']//a"

def get_html(main_link, header, block_url):
    regex_1 = re.compile(r'^\/')
    regex_2 = re.compile(r'^\/\/')
    response = requests.get(main_link, headers=header).text
    tree = html.fromstring(response)
    dict_news = dict()
    news_list = tree.xpath(block_url)
    list_news = list()
    for k in news_list:
        if regex_2.search(''.join(k.xpath("./@href"))):
            pass
        elif regex_1.search(''.join(k.xpath("./@href"))):
            h = main_link.replace('/news/', '') + ''.join(k.xpath("./@href"))
            list_news.append({'date': str(datetime.now()), 'resource': main_link, 'name':''.join(k.xpath("./text()")).strip().replace(u'\xa0', u' '), 'url': h})
        else:
            h = ''.join(k.xpath("./@href"))
            dict_news[''.join(k.xpath("./text()")).strip()] = h
            list_news.append({'date': str(datetime.now()), 'resource': main_link,'name':''.join(k.xpath("./text()")).strip(), 'url': h})
    return list_news
pprint(get_html(main_link_lenta, header_moz, block_url_lenta))
pprint(get_html(main_link_mail, header_moz, block_url_mail))
pprint(get_html(main_link_ya, header_moz, block_url_ya))

list_lenta = get_html(main_link_lenta, header_moz, block_url_lenta)
list_mail = get_html(main_link_mail, header_moz, block_url_mail)
list_ya = get_html(main_link_ya, header_moz, block_url_ya)

def to_db(list_name):
    client = MongoClient('localhost', 27017)
    db = client['news_database']
    collection = db.news_collection
    db.collection.insert_many(list_name)

to_db(list_lenta + list_mail + list_ya)
