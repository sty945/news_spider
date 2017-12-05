# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/12/4 22:55
# Author: sty
# File: splitfile.py
# 功能：
'''
主要是由于中科院计算所的NLPIR分词系统只能分割5000k以内的数据(实际只有490k),
所以不得不对大容量的txt文件进行分割成500k以下的文件
'''

import os
import time
import codecs

def split_file(file_name, filepath):
    '''
    输出文件500k大小的文件 read(len) len表示一个字符，GBK编码下一个汉字为2个字节
    故定义lensize = 256000 表示读取256000个字符，这些字符在最后存在GBK文件里的时候
    文件大小为：256000 * 2 / 1024 = 500k，实际情况下可能里面有一些英文字符所以实际大小为
    490k左右，再测试发现再少1024个字符结果在分词处理时效果更好
    :param file_name: 要分割文件的名字
    :param filepath: 分割文件存放路径
    :return:
    '''
    url_list = []
    print(file_name)
    with codecs.open(file_name, 'r', 'utf-8') as f:
        lensize = 256000 - 1024
        count = 0
        words = f.read().strip()
        print('file size :', len(words), ' type is ', type(words))
        i = 0
        while i < len(words) - lensize:
            url_list.append(words[i : i + lensize])
            i = i + lensize
            ouput_file_name = filepath + str(count) + '.txt'
            with codecs.open(ouput_file_name, "w", 'gbk') as file:
                s = str(url_list)
                # NLPIR分词系统只支持GBK的编码，将utf-8格式文本转换成gbk,坑
                res = s.encode('utf-8', 'ignore').decode('utf-8', 'ignore').encode('gbk', 'ignore').decode('gbk', 'ignore')
                file.write(res)
            url_list = []
            count += 1
    url_list.append(words[i: -1])
    ouput_file_name = filepath + str(count) + '.txt'
    # print(i)
    # print(url_list)
    # print(ouput_file_name)
    with codecs.open(ouput_file_name, "w", 'gbk') as file:
        s = str(url_list)
        res = s.encode('utf-8', 'ignore').decode('utf-8', 'ignore').encode('gbk', 'ignore').decode('gbk', 'ignore')
        file.write(res)

def all_split_file():
    # 自动获得当前文件所在目录的父目录下的contents文件夹
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\contents\\'

    filename = ''
    filepath = ''
    # 设置要转换的文件，如果是range(1, 12)表示装换01content.txt-11content.txt
    # for i in range(1,12):
    for i in range(11, 12):
        file = ''
        if i < 10:
            file = '0' + str(i)
        else:
            file = str(i)
        file += 'content'
        filename = path + file + '.txt'
        filepath = path + file + '\\'
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        split_file(filename, filepath)

if __name__ == '__main__':
    begin = time.time()
    all_split_file()
    end = time.time()
    # 统计要花费的时间
    print("spent time is " + str(end - begin))