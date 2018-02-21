功能：
以中国新闻网社会新闻板块为抓取对象,通过关键词来分析新闻热点事件
http://www.chinanews.com/society.shtml
当前抓取了2017年11月份所有数据新闻数据，后期进行数据可视化分析
也可以自己在homework1.py设置要抓取的时间段
本项目开源地址：https://github.com/sty945/news_spider
可视化分析报告：
https://mp.weixin.qq.com/s/LOEuUQe9rsv87S8KISGHJg

运行环境：
系统:windows
python版本：python 3.6.3
数据库:mongoDB 3.4.9
分词系统：中科院ictclas分词系统 地址：https://github.com/sty945/NLPIR
分词系统文件转json地址: http://tools.jb51.net/code/excel_col2json


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
        
