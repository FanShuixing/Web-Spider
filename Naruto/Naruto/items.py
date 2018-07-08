# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NarutoItem(scrapy.Item):
    # define the fields for your item here like:
	dir_name = scrapy.Field()
	dir_link=scrapy.Field()
	img_url=scrapy.Field()
	img_path=scrapy.Field()