# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/12/4 22:55
# Author: sty
# File: countDatabase.py
# 功能：
'''
在抓取网页的过程中统计数据库中数据数目，可在运行main.py之后，在命令行运行：
python countDatabase.py
'''

import time
from homework1 import item_info,url_lists

while True:
    print("url_lists:" + str(url_lists.count()))
    print("item_info:" + str(item_info.count()))
    time.sleep(2)