from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field

from foodCrawlers.items import FoodcrawlersItem
from foodCrawlers.checker import checkAndExtract
from foodCrawlers.checker import unicodeToAscii
from foodCrawlers.foodItem import foodItem

import unicodedata
import string

items_per_row = 3

class ApolloBananaCatering(CrawlSpider):	
	name = 'apolloBananaCatering'
	allowed_domains = ['apollobananaleaf.com']
	start_urls = ['http://apollobananaleaf.com/index.php/']

	rules = (
		Rule(SgmlLinkExtractor(allow=(".*/index.php/[a-zA-Z]+")), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		item = FoodcrawlersItem()
		item['itemArray'] = {}
		
		categories = hxs.select( '//div[@class="item-page"]//span[@style="font-size: 12pt;"]/text()' ).extract()
		
		category = "Place"
		
		categoryStrings = []
		for i in range(len(categories)):
			categoryStrings.append( unicodeToAscii( categories[i] ) )
			print categoryStrings[i]
		
		# We select the rows
		rows = hxs.select( '//tbody/tr' ).extract()
		
		# we parse each row one by one
		for row in rows:
			rowSelector = HtmlXPathSelector( text = row )
			columns = rowSelector.select( '//td/text()' ).extract()
			for i in range(2):
				foodNameString = checkAndExtract( rowSelector, '//td/text()', i * items_per_row )
				
				if( foodNameString == "" ):
					continue
					
				foodIngredientsString = checkAndExtract( rowSelector, '//td/text()', i * items_per_row + 1 )
				
				if( foodIngredientsString == "" ):
					continue
					
				foodPriceString = checkAndExtract( rowSelector, '//td/text()', i * items_per_row + 2 )
				
				if( foodPriceString == "" ):
					continue
				
				fI = foodItem( foodNameString, category, foodIngredientsString, foodPriceString )
				item['itemArray'][foodNameString] = fI
				
				
		return item
