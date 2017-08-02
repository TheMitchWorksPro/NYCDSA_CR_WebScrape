# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CrComputersItem(scrapy.Item):
	prod_class = scrapy.Field()
	brand = scrapy.Field()
	model = scrapy.Field()
	spec_label = scrapy.Field()
	spec_value = scrapy.Field()
	url = scrapy.Field()