# -*- coding: utf-8 -*-
# Author:Alethia
import scrapy
import re
import time
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from douban_book.items import DoubanBookItem

''' This file implement a standard Spider file in scrapy'''

class DoubanspiderSpider(CrawlSpider):
	name = 'doubanSpider'
	allowed_domains = ['book.douban.com']
	start_urls = ['https://book.douban.com/top250/']

	rules = (
			Rule(LinkExtractor(allow = (r'https://book.douban.com/top250\?start=\d+'))),
			Rule(LinkExtractor(allow = (r'https://book.douban.com/subject/\d+')),callback = 'parse_book')
		)

	def parse_book(self, response):
		sel = Selector(response = response)
		item = DoubanBookItem()

		item["name"] = sel.xpath("//div[@id = 'wrapper']/h1/span/text()").extract_first().strip()
		item["score"]= sel.xpath("//*[@id='interest_sectl']/div/div[2]/strong/text()").extract_first().strip()
		item["link"] = response.url

		try:
			contents = sel.xpath("//*[@id='link-report']/div[1]/div/p/text()").extract()
			item["content_description"] = "\n".join(content for content in contents).strip()
		except:
			item["content_description"] = ""

		try:
			profiles = sel.xpath("//*[@id='content']/div/div[1]/div[3]/div[2]/div/div/p/text()").extract()
			item["author_profile"] = "\n".join(profile for profile in profiles).strip()
		except:
			item["author_profile"] = ""

		#get the infos of the book and processing the string to extract info
		infos = response.xpath("//*[@id='info']").extract_first()
		infos = re.sub("\s+","",infos)
		infos = re.sub("<.*?>"," ",infos).strip()
		infos = infos.split(" ")
		infos = [info.replace(":","") for info in infos if info != "" and info != ":" and info != " "]

		#extract info
		inventory = [("author","作者"),("press","出版社"),("date","出版年"),("page","页数"),("price","定价"),("ISBN","ISBN")]
		for dict_name,info_name in inventory:
			item[dict_name] = infos[infos.index(info_name) + 1] if info_name in infos else ""

		return item