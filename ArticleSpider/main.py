"""
main模块用于在pycharm中调试scrapy爬虫
"""


import sys
import os
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy" , "crawl" , "zhihu"]) # zhihu为爬虫名称, 爬取知乎