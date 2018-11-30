#main模块用于在pycharm中调试scrapy爬虫
from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy" , "crawl" , "jobbole"])#jobbole为爬虫名称, 爬取伯乐在线
execute(["scrapy" , "crawl" , "zhihu"])#zhihu为爬虫名称, 爬取知乎