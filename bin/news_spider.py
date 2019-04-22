# -*- coding: utf-8 -*-

# !/usr/bin/env python

# Time: 2019/4/17 22:17

# Author: sty

# File: news_spider.py

import requests
from bs4 import BeautifulSoup
import time
import re
import pymongo
import datetime
from newspaper import Article
from multiprocessing import Pool, Lock

client = pymongo.MongoClient('localhost', 27017)
news = client['chinanews']
# 页面详细信息表
item_info = news['item_info']
# 网页连接URL
url_lists = news['url_lists']
badcase_url_lists = news['badcase_url_lists']


def get_day_list(start='2018-01-01', end='2018-12-31'):
    '''
    得到设置时间段内的所有时间日期
    :return:以列表形式返回所有时间日期
    '''
    daylist = []    # daylist 存放这个时间段所有的日期

    # 将日期格式化
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        daylist.append(datestart.strftime('%m%d'))
    return daylist

def get_single_links(url, web_site='http://www.chinanews.com'):
    try:
        # 加入代理头
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'}
        wb_data = requests.get(url, headers=headers)
        wb_data.encoding = wb_data.apparent_encoding
        soup = BeautifulSoup(wb_data.text, 'lxml')
        links = soup.select('div.dd_bt > a')
        for link in links:
            link = link.get('href')
            url_arr = url.split('/')
            year = url_arr[-3]
            month = url_arr[-2][:2]
            day = url_arr[-2][2:]
            if web_site not in link:
                res_link = web_site + link
            data = {
                "link": res_link,
                "date":{
                    "year": year,
                    "month": month,
                    "day": day
                }
            }
            url_lists.insert_one(data)
    except:
        print("get_single_links error")


def get_single_links_regrex(url):
    try:
        # 加入代理头
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'}
        wb_data = requests.get(url, headers=headers)
        wb_data.encoding = wb_data.apparent_encoding
        soup = BeautifulSoup(wb_data.text, 'lxml')
        # print(soup)
        # 取出网页链接的正则
        link_ptn = r"url\S*source"
        single_links = re.findall(link_ptn, soup.text)
        for link in single_links:
            # 网页链接结果处理操作
            link = link.replace('url":"', '')
            link = link.replace('","source', '')
            link = link.replace('\\', '')
            # all_links.append(link)
            data = {
                "link": link,
                "year": link.split('/')[-3],
                "month": link.split('/')[-2].split('-')[0],
                "day": link.split('/')[-2].split('-')[1]
            }
            url_lists.insert_one(data)
    except:
        print("get_single_links_regrex error")


def get_all_links(urls):
    for url in urls:
        time.sleep(0.3)
        get_single_links(url)
        print("current database count:" + str(url_lists.count()))

def get_link_article(url,is_deal_badcase=False):
    try:
        if not is_deal_badcase:
            lock.acquire()
        article = Article(url, language='zh')  # Chinese
        # 网页下载
        article.download()
        if not is_deal_badcase:
            lock.release()
        # 网页解析
        article.parse()
        # 获取文章内容
        text = article.text.strip()
        # 替换换行符
        text = text.replace('\n\n', '')
        data = {
            "link": url,
            "content": text,
            "date":{
                "year": url.split('/')[-3],
                "month": url.split('/')[-2].split('-')[0],
                "day": url.split('/')[-2].split('-')[1]
            }
        }
        item_info.insert_one(data)
        print(data)
        if badcase_url_lists.find({"link":url}).count() > 0:
            badcase_url_lists.remove({"link":url})
        # print(data)
    except:
        badcase_data = {
            "link": url
        }
        if badcase_url_lists.find(badcase_data).count() == 0:
            badcase_url_lists.insert_one(badcase_data)
        print("get_link_article error")

def get_link_info(url):
    '''
    从单个新闻的链接中得到这个链接中的新闻内容
    :param url: 单个新闻的链接
    :return:
    '''
    try:
        contentTxt = ""
        wb_data = requests.get(url)
        wb_data.encoding = wb_data.apparent_encoding
        print(wb_data.apparent_encoding)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        contents = soup.select('.left_zw > p')
        for content in contents:
            contentTxt += content.get_text().strip()
        # print(''.join(contentTxt.encode('utf8').decode('utf8').split('')))
        # print(''.join(contentTxt))
        contentTxt = contentTxt.encode('utf-8').decode('utf-8')
        data = {
            "link": url,
            "content": contentTxt,
            "date":{
                "year": url.split('/')[-3],
                "month": url.split('/')[-2].split('-')[0],
                "day": url.split('/')[-2].split('-')[1]
            }
        }
        item_info.insert_one(data)
        print(data)
    except:
        print("get_link_info error")

def all_links_from_db():
    all_links = []
    for data in url_lists.find():
        all_links.append(data['link'])
    return all_links

def init(l):
	global lock
	lock = l

def deal_failed_url():
    all_links = []
    for data in badcase_url_lists.find():
        all_links.append(data['link'])
    for link in all_links[:]:
        get_link_article(link,True)

if __name__ == '__main__':
    # 设置获取数据的时间区间
    day_lists = get_day_list('2019-02-28', '2019-3-31')
    # 得到在约定时间区间之中的
    urls = ['http://www.chinanews.com/scroll-news/2019/{}/news.shtml'.format(day) for day in day_lists]
    get_all_links(urls)
    lock = Lock()
    pool = Pool(3, initializer=init, initargs=(lock,))  # 创建多线程池
    pool.map(get_link_article, all_links_from_db())
    pool.close()
    pool.join()

    # 如果badcase库中数据量超过1000则持续解决
    while badcase_url_lists.count() >= 100:
        deal_failed_url()
