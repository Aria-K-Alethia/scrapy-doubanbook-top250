# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# Author:Alethia

import scrapy
from scrapy.item import Item,Field

''' This file define the class of Item '''


class DoubanBookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    author = Field()
    press = Field()
    date = Field()
    page = Field()
    price = Field()
    score = Field()
    ISBN = Field()
    author_profile = Field()
    content_description = Field()
    link = Field()
    