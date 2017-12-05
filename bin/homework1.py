# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/12/4 22:55
# Author: sty
# File: homework1.py
# 功能：
'''
主要实现页面链接和新闻的爬取，是爬虫的主要内容
'''
import requests
from bs4 import BeautifulSoup
import time
import pymongo
import datetime

# 连接mongoDB数据库,并建立信息数据库，这里建立了11月份的数据库
client = pymongo.MongoClient('localhost', 27017)
news = client['chinanews11']
# 页面详细信息表
item_info = news['item_info']
# 网页连接URL
url_lists = news['url_lists']


def get_day_list():
    '''
    得到设置时间段内的所有时间日期
    :return:以列表形式返回所有时间日期
    '''
    daylist = []    # daylist 存放这个时间段所有的日期
    # 设置了11月的起止日起
    start = '2017-11-01'
    end = '2017-11-30'

    # 将日期格式化
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        daylist.append(datestart.strftime('%m%d'))
    return daylist

def get_single_links(url):
    '''
    通过某一天的主页面URL得到该页面下的所有URL，并将URL存入到url_list的表中去
    :param url: 某天的主页面
    :return:
    '''
    try:
        # 基本抓取流程
        wb_data = requests.get(url)
        #print(wb_data.status_code)
        wb_data.encoding = wb_data.apparent_encoding
        soup = BeautifulSoup(wb_data.text, 'lxml')
        links = soup.select('li > .dd_bt > a') #获取链接所在的标签获得链接
        for link in links:
            #print(link.get('href'))
            url_lists.insert_one({'links': link.get('href')}) #将链接插入到数据库中去
    except:
        print("error")

def get_all_links():
    '''
    通过之前的时间段数据得到该时间段对应当天页面，然后通过get_single_links得到该页面下的所有链接，
    以此来循环得到这段时间所有新闻的所有的链接
    :return:
    '''
    daylist = get_day_list() #获取时间段
    # 所有时间段对应的页面
    urls = ['http://www.chinanews.com/scroll-news/sh/2017/{}/news.shtml'.format(day) for day in daylist]
    # 从所有时间段页面找到每个新闻的页面
    for url in urls:
        print(url)
        time.sleep(0.5)
        get_single_links(url)
        print("current database count:" + str(url_lists.count()))

def get_res(url):
    '''
    从单个新闻的链接中得到这个链接中的新闻内容
    :param url: 单个新闻的链接
    :return:
    '''
    try:
        contentTxt = ""
        wb_data = requests.get(url)
        wb_data.encoding = wb_data.apparent_encoding
        soup = BeautifulSoup(wb_data.text, 'lxml')
        contents = soup.select('.left_zw > p')
        for content in contents:
            contentTxt += content.get_text().strip()
        data = {
            "link": url,
            "content": contentTxt,
            "year": url.split('/')[-3],
            "month": url.split('/')[-2].split('-')[0],
            "day": url.split('/')[-2].split('-')[1]
        }
        item_info.insert_one(data)
        print(data)
    except:
        print("error")

