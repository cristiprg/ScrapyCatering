# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.contrib.exporter import XmlItemExporter
from scrapy import signals
from FoodXmlItemExporter import FoodXmlItemExporter

class FoodcrawlersPipeline(object):

	def __init__(self):
		self.allSpiceCateringPossibleCategories = ['heartybreakfast', 'centerpieceentreesalads', 'casualluncheon', 'sandwicheslunchboxes', 'enticingentrees', 'hotentrees', 'vegetarianmenu', 'soupschili', 'hotcoldappetizers', 'temptingdesserts']

	def process_item(self, item, spider):
	
		if spider.name == 'allSpiceCatering':
			if not item['foodName']:
				raise DropItem("Missing foodName in %s" % item)
			if not item['category'] in self.allSpiceCateringPossibleCategories:
				raise DropItem("Invalid category in %s" % item)
	
		return item
	

class XmlExportPipeline(object):

	def __init__(self):
		self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		file = open('%s_products.xml' % spider.name, 'w+b')
		self.files[spider] = file
		self.exporter = FoodXmlItemExporter(file)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
