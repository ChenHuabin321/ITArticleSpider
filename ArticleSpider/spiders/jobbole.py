# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy.http import Request
from ArticleSpider.items import JobboleArticleItem , ArticleItemLoader
from scrapy.loader import ItemLoader

from ArticleSpider.utils import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的url，并交给解析函数进行具体字段解析
        2. 获取下一页的URL，并交给scrapy进行下载，下载完成后交给parse
        """
        # 获取文章列表页中的url，并交给解析函数进行具体字段解析
        post_nodes = response.xpath('//*[@id="archive"]//div[@class="post floated-thumb"]/div[1]/a[1]')
        for post_node in post_nodes:
            front_image_url = post_node.xpath('img/@src').extract_first("")#xpath的嵌套使用
            post_url = post_node.xpath('@href').extract_first("")
            # 有时刚抓取到的url没有完整的域名，例如：/article/123
            # 这时候需要加上域名拼凑完整的url链接时，可以如下操作
            # from urllib import parse  # 获取当前页域名
            # whole_url = parse.urljoin(response.url , post_url)
            ####################################################################
            # 回调parse_detail函数，抓取每篇文章详细字段（三级页面字段）
            yield Request(url=post_url, meta={"front_image_url":front_image_url} , callback=self.parse_detail)# 发送下载中间件进行下载并进行解析
            ####################################################################

            ####################################################################
            # 以下两行代码等效，都是取出第一个元素，
            # 但是推荐使用extract_first，因为就算没有提取到数据，也只是返回None
            # 但是extract()[0]的方式会返回异常

            # next_url = response.xpath('//*[@class="next page-numbers"]/@href').extract()[0]
            next_url = response.xpath('//*[@class="next page-numbers"]/@href').extract_first()
            if next_url:# 继续爬取下一列表页（下一个二级页）
                yield Request(url=next_url , callback=self.parse)


    def parse_detail(selfself , response):
        """
        提取文章的具体字段
        :param response:
        :return:
        """
####################################数据抓取方法一：通过直接赋值item#####################################################
        # 封面图
        article_item = JobboleArticleItem()
        front_image_url = response.meta.get("front_image_url" , "")
        # 标题
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()

        # 创建日期
        create_date = response.xpath('//*[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace('·','').replace(' ' ,'')
       # 点赞数量
        praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first())
        # 收藏数
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        match_re = re.match('.*?(\d+).*' , fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        #评论数
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        match_re = re.match('.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        # 正文内容
        content = response.xpath("//div[@class='entry']").extract_first('')
        # 文章标签
        tag_list = response.xpath('//*[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        tags = ','.join(tag_list)
        try:
            create_date = datetime.datetime.strptime(create_date,"%Y%m%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['title'] = title
        article_item['url_object_id'] = get_md5(response.url)
        article_item['url'] = response.url
        article_item['create_date'] = create_date
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['comment_nums'] = comment_nums
        article_item['fav_nums'] = fav_nums
        article_item['tags'] = tags
        article_item['content'] = content
#############################数据抓取方法二：通过item loader加载item###############################################################
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobboleArticleItem() , response=response)
        item_loader.add_xpath('title' , '//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('create_date' , '//*[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_xpath('praise_nums' , "//span[contains(@class,'vote-post-up')]/h10/text()")
        item_loader.add_xpath('fav_nums' , '//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('comment_nums' , "//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath('content' , "//div[@class='entry']")
        item_loader.add_xpath('tags' , '//*[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        article_item = item_loader.load_item()
        yield article_item


