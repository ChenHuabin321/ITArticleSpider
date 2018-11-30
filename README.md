# ITArticleSpider

---
## 1. 项目介绍
### 1.1 基本情况
本爬虫用于采集**伯乐在线**等知名IT相关网站中的文章，可用于分析时下IT热点话题及热门技术走向。
项目中代码有详细的注释，方便日后代码review，并对部分功能用不同方法进行实现，方便学习。
### 1.2 下载
- 下载源码

    git方式下载：git@github.com:ChenHuabin321/ITArticleSpider.git

    或者直接到下载zip源码包，地址为：https://github.com/ChenHuabin321/ITArticleSpider
- 安装依赖

    PyMySQL==0.9.2

    Scrapy==1.5.0

    Twisted==18.4.0
- 数据库配置

    以下是settings.py中的默认数据库配置，可进行修改为你的数据库配置：

    MYSQL_HOST = '192.168.56.101'#主机

    MYSQL_PASSWORD = '123456'#密码

    MYSQL_DBNAME = 'article_spider'#数据库名

---

## 2. 伯乐在线网站爬虫
### 2.1 采集字段
采集字段包括包含文章标题、发布时间、文章标签、正文内容，评论数、收藏数、点赞数等字段信息。
### 2.2 技术路线
伯乐在线文章爬虫基于scrapy爬虫框架编写，数据存储是采用scrapy自带的异步存储的方式存储在在MySQL数据库中，数据抓取用的是xpath+正则的方法。
### 2.3 数据库设计及结果展示
伯乐在线文章爬虫数据库结构设计如下图所示：
![伯乐在线文章爬虫数据库结构设计](https://github.com/ChenHuabin321/ITArticleSpider/blob/master/git_images/jobboe_database.png)

伯乐在线文章爬虫结果如下图所示：
![伯乐在线文章爬虫结果展示](https://github.com/ChenHuabin321/ITArticleSpider/blob/master/git_images/jobbole_data.png)

