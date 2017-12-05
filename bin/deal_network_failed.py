# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/12/4 22:55
# Author: sty
# File: deal_network_failed.py
# 功能：
'''
在抓取网页的过程中可能会出现网络中断的情况，所以为了下次不再重复抓取，设置一个断点续传
'''

from multiprocessing import Pool
from homework1 import news, get_res, get_all_links, item_info, url_lists

def all_links():
    '''
        从链接数据库里面读取所有链接
        从结果数据库里面读取所有链接
        然后取他们的差集
        :return: 以所有链接的列表形式
    '''
    db_urls = []
    index_urls = []
    for url in url_lists.find():
        db_urls.append(url['links'])
    for url in item_info.find():
        index_urls.append(url['link'])
    print(len(db_urls))
    print(len(index_urls))
    #设置了两个集合，x是所有URL的集合，y是已经抓取的URL的集合，将他们取差集
    x = set(db_urls)
    y = set(index_urls)
    rest_of_urls = x - y
    return  rest_of_urls

if __name__ == '__main__':
    pool = Pool()
    pool.map(get_res, all_links())

