from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field

from foodCrawlers.items import FoodcrawlersItem
from foodCrawlers.checker import checkAndExtract
from foodCrawlers.foodItem import foodItem

import unicodedata
import string

items_per_row = 3

class ArianaCatering(CrawlSpider):	
	name = 'arianaCatering'
	allowed_domains = ['ariana2restaurant.co.uk']
	start_urls = ['http://www.ariana2restaurant.co.uk/menu.html']

	rules = (
		Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		item = FoodcrawlersItem()
		item['itemArray'] = {}
		
		category = "PlaceHolder"
		
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
