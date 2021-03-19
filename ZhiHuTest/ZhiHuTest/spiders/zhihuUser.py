# -*- coding: utf-8 -*-
import scrapy
from ..items import ZhihutestItem
import json
class ZhihuuserSpider(scrapy.Spider):
    name = 'zhihuUser'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']

    start_user = 'zhang-jia-wei'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):  ##当spider启动爬取并且未指定start_urls时，该方法被调用
        user = self.start_user
        url = self.user_url.format(user=user, include=self.user_query)
        yield scrapy.Request(url, self.parseUser)
        yield scrapy.Request(self.follows_url.format(user=user, include=self.follows_query, limit=20, offset=0),
                      self.parseFollows)
        yield scrapy.Request(self.followers_url.format(user=user, include=self.followers_query, limit=20, offset=0),
                      self.parseFollowers)

    def parseUser(self, response):
        item = ZhihutestItem()
        result = json.loads(response.text)
        # self.DealResult(result)  # 处理educations，employments，business，locations，badge
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        if item["follower_count"] > 0:
            yield scrapy.Request(
                self.follows_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0),
                self.parseFollows)
        if item['follower_count'] == 0:
            yield scrapy.Request(
                self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20,
                                          offset=0), self.parseFollowers)
    # def start_requests(self):
    #       # 这里我们传入了将选定的大V的详情页面的url，并指定了解析函数parseUser
    #     yield scrapy.Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parseUser)
    #     yield scrapy.Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
    #                          callback=self.parseFollows)
    #     yield scrapy.Request(
    #     self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20),
    #     callback=self.parseFollowers)
    # def parseUser(self, response):
    #     # print(type(response.text))
    #       # 这里页面上是json字符串类型我们使用json.loads（）方法将其变为文本字符串格式
    #     result = json.loads(response.text)
    #     # print(result)
    #     item = ZhihutestItem()
    #     for field in item.fields:
    #         if field in result.keys():
    #             item[field] = result.get(field)
    #     # yield item
    #     # print(item)
    #     # print(type(item))
    #     yield scrapy.Request(
    #     self.follows_url.format(user=result.get('url_token'), include=self.follows_query, offset=0, limit=20),callback=self.parseFollows)
    #     yield scrapy.Request(
    #     self.followers_url.format(user=result.get('url_token'), include=self.followers_query, offset=0, limit=20),callback=self.parseFollowers)
    def parseFollows(self, response):
        results = json.loads(response.text)
      # 判断data标签下是否含有获取的文本字段的keys
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                                 callback=self.parseUser)
      # 判断页面是否翻到了最后
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page, callback=self.parseFollows)
    def parseFollowers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                             callback=self.parseUser)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page, callback=self.parseFollowers)