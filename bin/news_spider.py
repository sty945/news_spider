# -*- coding: utf-8 -*-

# !/usr/bin/env python

# Time: 2019/4/17 22:17

# Author: sty

# File: news_spider.py

import requests
from bs4 import BeautifulSoup
import time
import pymongo
import datetime
from newspaper import Article
from multiprocessing import Pool, Lock

client = pymongo.MongoClient('localhost', 27017)
news = client['chinanews']
# 页面详细信息表
item_info = news['item_info']
# 网页链接URL
url_lists = news['url_lists']
# 爬取失败网页链接URL
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
    while datestart <= dateend:
        daylist.append(datestart.strftime('%m%d'))
        datestart += datetime.timedelta(days=1)
    return daylist

def get_single_links(url, web_site='http://www.chinanews.com'):
    """
    :param url:需要抓取的网页
    :param web_site: 主站点
    :return:
    """
    try:
        # 加入代理头
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'}
        # 获取网页数据
        wb_data = requests.get(url, headers=headers)
        # 指定网页编码
        wb_data.encoding = wb_data.apparent_encoding
        # 解析网页
        soup = BeautifulSoup(wb_data.text, 'lxml')
        # 通过css selector获取网页链接所在的元素块
        links = soup.select('div.dd_bt > a')
        # 遍历元素块列表
        for link in links:
            # 获取网页
            link = link.get('href')
            # 获取该网页对应的时间信息
            url_arr = url.split('/')
            year = url_arr[-3]
            month = url_arr[-2][:2]
            day = url_arr[-2][2:]
            # 为不包含网页域名的网址加上网页域名
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
            # 将数据存储到数据库
            url_lists.insert_one(data)
    except:
        print("get_single_links error")

def get_all_links(urls):
    """
    :param urls:列表页的集合
    :return:
    """
    for url in urls:
        # 为了防止反爬虫，睡眠0.3s
        time.sleep(0.3)
        get_single_links(url)
        print("current database count:" + str(url_lists.count()))

def get_link_article(url,is_deal_badcase=False):
    """
    抓取网页内容函数
    :param url: 网址
    :param is_deal_badcase:是否是之前抓取失败了
    :return:
    """
    try:
        # 如果是处理badcase_url则不加锁
        if not is_deal_badcase:
            lock.acquire()
        article = Article(url, language='zh')  # Chinese
        # 网页下载
        article.download()
        # 如果是处理badcase_url则不加锁
        if not is_deal_badcase:
            lock.release()
        # 网页解析
        article.parse()
        # 获取文章内容
        text = article.text.strip()
        # 替换换行符
        text = text.replace('\n\n', '')
        # 构造data数据形式
        data = {
            "link": url,
            "content": text,
            "date":{
                "year": url.split('/')[-3],
                "month": url.split('/')[-2].split('-')[0],
                "day": url.split('/')[-2].split('-')[1]
            }
        }
        # 在item_info表中插入数据
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

def all_links_from_db():
    """
    获取数据库中数据
    :return:
    """
    all_links = []
    for data in url_lists.find():
        all_links.append(data['link'])
    return all_links

def init(l):
	global lock
	lock = l

def deal_failed_url():
    """
    处理为爬取成功的数据
    :return:
    """
    all_links = []
    for data in badcase_url_lists.find():
        all_links.append(data['link'])
    for link in all_links[:]:
        get_link_article(link,True)

if __name__ == '__main__':
    # 设置获取数据的时间区间
    day_lists = get_day_list('2019-03-01', '2019-3-31')
    # 得到在约定时间区间之中的列表页集合
    urls = ['http://www.chinanews.com/scroll-news/2019/{}/news.shtml'.format(day) for day in day_lists]
    get_all_links(urls)
    # 加锁
    lock = Lock()
    # 创建进程池
    pool = Pool(3, initializer=init, initargs=(lock,))  # 创建多线程池
    pool.map(get_link_article, all_links_from_db())
    # 回收进程池
    pool.close()
    pool.join()

    # 如果badcase库中数据量超过1000则持续解决
    while badcase_url_lists.count() >= 100:
        deal_failed_url()
