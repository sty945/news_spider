## 基于新闻媒体的热点新闻数据可视化分析
欢迎对数据可视化、数据挖掘感兴趣的同学一起完成这个项目。
**welcome to fork**

## 当前功能：

以中国新闻网社会新闻板块为抓取对象,通过关键词来分析新闻热点事件:
[中国新闻网链接](http://www.chinanews.com/society.shtml)

当前代码中设置的是抓取2017年11月份所有数据新闻数据，后期进行数据可视化分析，用户也可以自己在homework1.py设置要抓取的时间段

[本项目开源地址](https://github.com/sty945/news_spider)

[当前结果展示](https://github.com/sty945/news_spider/blob/master/result/news_spider_vision.ipynb)

[可视化分析报告](https://mp.weixin.qq.com/s/LOEuUQe9rsv87S8KISGHJg)

## 预期实现功能
建立一整套从新闻信息挖掘到分析以及可视化展现的完整体系，
使用户能够很好的关注整个当前的新闻热点以及这些热点的起始、 经过、 发展和消逝的整个过程。

微信官方曾经关于新闻热点可视化的一篇推送，可做参考:

[微信小秘密: 2016 年那些 10w+ 文章是怎么刷爆朋友圈的？](http://mp.weixin.qq.com/s/hlWAW8UybzF5jzhNyRx_Bg)

## 国内常用热搜榜
[微博热搜](http://s.weibo.com/top/summary?cate=homepage)
[百度热搜风云榜](http://top.baidu.com/)
[搜狗热搜榜](http://top.sogou.com/)
[360实时热点](https://trends.so.com/hot)
[360趋势](https://trends.so.com/)


## 运行环境：
系统:windows

python版本：python 3.6.3

数据库:mongoDB 3.4.9

分词系统：中科院ictclas分词系统 地址：https://github.com/sty945/NLPIR

分词系统文件转json地址: http://tools.jb51.net/code/excel_col2json

## 目录下文件功能解释
```
news_spider
│  readme.txt
│  
├─bin
│  │  countDatabase.py     在数据抓取过程中统计数据库中数据数量
│  │  deal_network_failed.py    解决抓取过程中，网络掉线或者其他中断情况的断点续传功能
│  │  homework1.py    爬虫主程序
│  │  main.py   运行主程序
│  │  splitfile.py   将很大的txt文件分割成若干个指定大小的小txt文件
│  │  writefile.py   将数据库中所有的新闻数据写入到txt文本中
│  │  
│  └─__pycache__    缓存文件
│          homework1.cpython-36.pyc
│          
├─contents
│  │  11content.txt   2017年11月份的结果数据文本
│  │  
│  └─11content       2017年11月份的结果数据文本（分割后的小文件）
│          0.txt
│          1.txt
│          10.txt
│          11.txt
│          12.txt
│          13.txt
│          14.txt
│          15.txt
│          16.txt
│          2.txt
│          3.txt
│          4.txt
│          5.txt
│          6.txt
│          7.txt
│          8.txt
│          9.txt
│          
└─result      结果存放
        11month_view .html    数据可视化展示，基于jupyter notebook 书写保存后的html，建议firefox打开，chrome图表显示有问题
        11result.json        处理后的用json保存的数据提取出来关键词结果
        raw_result.json      处理前的用json保存的数据提取出来关键词结果
        news_spider_vision.ipynb jupyter note格式的结果展示
```     
