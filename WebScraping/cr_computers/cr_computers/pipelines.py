# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

# class CrValidateItemPipeline(object):
# 	def process_item(self, item, spider):
# 		if not all(item.values()):
# 			raise DropItem("Missing values!")
# 		else:
# 			return item

class CrWriteItemPipeline(object):
	def __init__(self):
		self.filename = 'cr_spider_specs.csv'

	def open_spider(self, spider):
		self.csvfile = open(self.filename, 'wb')
		self.exporter = CsvItemExporter(self.csvfile)
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.csvfile.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item

# class CrComputersPipeline(object):
#     def process_item(self, item, spider):
#         return item
