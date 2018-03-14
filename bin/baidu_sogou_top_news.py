# !/usr/bin/env python

# -*- coding: utf-8 -*-

# Time: 2018/3/13 14:41

# Author: sty

# File: baidu_sogou_top_news.py

import requests
from bs4 import BeautifulSoup
import time
import pymongo
from datetime import datetime

client = pymongo.MongoClient('localhost', 27017)


# 创建sogou，baidu 热搜榜的数据库
def create_sogou_db(current_time, current_day, db_soure):
    """
    :param current_time: 当前时间
    :param db_soure: sogou.baidu
    :return: 当前时间对数据库中的表
    """
    current_time_list = current_time + '_list'
    db_soure_name = db_soure + '_name'
    if db_soure == 'baidu':
        baidu_top_news = client[db_soure_name]
        baidu_top_list = baidu_top_news[current_time_list]
    if db_soure == 'sogou':
        current_day_list = current_day + '_list'
        sogou_top_news = client[db_soure_name]
        shishi_top_list = sogou_top_news[current_time_list]
        sevendsnews_top_list = sogou_top_news[current_day_list]
        return shishi_top_list, sevendsnews_top_list
    return []

def get_sogou_single_links(url, db):
    try:
        wb_data = requests.get(url)
        wb_data.encoding = wb_data.apparent_encoding
        soup = BeautifulSoup(wb_data.text, 'lxml')
        contents = soup.select('.pub-list > li > .s2')
        # print(contents)
        for content in contents:
            print(content.find('href'))
        #     data = {
        #         'title': content.select('.s2>.p1>a')[0].get_text(),
        #         'link': content.select('.s2>.p1>a')[0].get('href'),
        #         'mark': content.select('.s3')[0].get_text()
        #     }
        #     print(data)
            # db.insert_one(data)
    except:
        print("error")


def get_sogou_links():
    current_time = datetime.now().strftime('%Y-%m-%d-%H')
    current_day = datetime.now().strftime('%Y-%m-%d')
    sogou_sevendsnews_links = ['http://top.sogou.com/hot/sevendsnews_{}.html'.format(num) for num in range(1, 4)]
    sogou_shishi_links = ['http://top.sogou.com/hot/shishi_{}.html'.format(num) for num in range(1, 2)]
    shishi_top_list, sevendsnews_top_list = create_sogou_db(current_time, current_day, 'sogou')
    for link in sogou_shishi_links:
        print(link)
        get_sogou_single_links(link, shishi_top_list)

get_sogou_links()
