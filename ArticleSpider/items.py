# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import datetime
import scrapy
from scrapy.loader.processors import MapCompose # 在item中对提取到的值进行进一步处理
from scrapy.loader.processors import TakeFirst # 只取取出的第一个值
from scrapy.loader.processors import Join # 列表连接
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value+"-jobbole"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y%m%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    """
    取出tag中的评论
    :param value:
    :return:
    """
    if '评论' in value:
        return ""
    else:
        return value


def return_value(value):
    """
    本函数什么都不做，只是用于覆盖ArticleItemLoader，让系统不会使用该类处理某个item
    :param value:
    :return:
    """
    return value


class ArticleItemLoader(ItemLoader):
    """
    自定义的ItemLoader
    """
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert) ,
        # output_processor=TakeFirst()#设置输出的时候只取第一个，已在ArticleItemLoader中设置，此处可省略
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)#设置了output_processor之后，就不会再使用ArticleItemLoader的默认设置了
    )
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    tags = scrapy.Field(
        output_processor=Join(',')
    )
    content = scrapy.Field()


