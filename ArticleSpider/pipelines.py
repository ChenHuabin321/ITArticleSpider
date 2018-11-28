# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json' , 'w' , encoding='utf-8')
    def process_item(self, item, spider):
        lines = json.dumps(dict(item) , ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self , spider):#这个函数在爬虫关闭的时候回自动调用
        self.file.close()

class JsonEporterPipleline(object):
    # 调用scrapy提供的json export到处json文件
    def __init__(self):
        self.file = open('articleexpor.json' , 'wb')
        self.exporter = JsonItemExporter(self.file , encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self , spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



class ArticlepiderPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok , value in results:
            image_file_path = value['path']
        item["front_image_path"] = image_file_path
        return item

class MysqlPipeline(object):
    def __init__(self):
        host = '119.29.215.39'
        user = 'root'
        password = '123456'
        dbname = 'article_spider'
        self.conn = MySQLdb.connect(host , user , password ,
                                    dbname , charset='utf8' , use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self , item , spider):
        insert_sql = """
        insert into jobbole_article(
        title , url_object_id, url , create_date , front_image_url, front_image_path, praise_nums, comment_nums, fav_nums,tags,content)
        VALUES (%s , %s, %s, %s,%s , %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql , (
            item['title'],
            item['url_object_id'],
            item['url'],
            item['create_date'],
            item['front_image_url'],
            item['front_image_path'],
            item['praise_nums'],
            item['comment_nums'],
            item['fav_nums'],
            item['tags'],
            item['content']
        ))
        self.conn.commit()

class MysqlTwistedPipline(object):
    def __init__(self , dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls, settings):#读取配置
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            db = settings['MYSQL_DBNAME'],
            charset='utf8',
            cursorclass='MySQLdb.cursors.DictCursor',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)
    def process_item(self , item , spider):
        """
        使用twisted将mysql插入编程异步执行
        :param item:
        :param spider:
        :return:
        """
        query = self.dbpool.runInteraction(self.do_insert , item)
        query.addErrback(self.handle_error)
    def handle_error(self , failure):
        print(failure)
    def do_insert(self, item):
        """
        执行具体插入
        :param item:
        :return:
        """
        insert_sql = """
                insert into jobbole_article(
                title , url_object_id, url , create_date , front_image_url, front_image_path, praise_nums, comment_nums, fav_nums,tags,content)
                VALUES (%s , %s, %s, %s,%s , %s, %s, %s, %s, %s, %s)
                """
        self.cursor.execute(insert_sql, (
            item['title'],
            item['url_object_id'],
            item['url'],
            item['create_date'],
            item['front_image_url'],
            item['front_image_path'],
            item['praise_nums'],
            item['comment_nums'],
            item['fav_nums'],
            item['tags'],
            item['content']
        ))


class MysqlTwistedPipline2(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常
        print('********************************************')
        print(type(item['content']))

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
                        insert into jobbole_article(
                        title , url_object_id, url , create_date , front_image_url, praise_nums, comment_nums, fav_nums,tags,content)
                        VALUES (%s , %s, %s, %s,%s , %s,  %s, %s, %s, %s)
                        """
        cursor.execute(insert_sql, (
            item['title'],
            item['url_object_id'],
            item['url'],
            item['create_date'],
            item['front_image_url'],
            # item['front_image_path'],
            item['praise_nums'],
            item['comment_nums'],
            item['fav_nums'],
            item['tags'],
            item['content']
        ))


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self , results , item , info ):
        if "front_image_url" in item:
            for ok , value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item