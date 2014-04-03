from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field

from foodCrawlers.items import FoodcrawlersItem
from foodCrawlers.utils import checkAndExtract
from foodCrawlers.utils import unicodeToAscii
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
		
		if( categories == [] ):
			categories = hxs.select( '//div[@class="item-page"]//strong/text()' ).extract()
		
		
		categoryStrings = []
		for i in range(len(categories)):
			categoryStrings.append( unicodeToAscii( categories[i] ) )
			print categoryStrings[i]
		
		# We select the rows
		tableSelectors = hxs.select( '//table' )
		index = 0;
		
		# we parse each row one by one
		for tableSel in tableSelectors:
			tableEntries = tableSel.select( '//td/text()' ).extract()
			numberOfRows = len( tableEntries ) / items_per_row
			for i in range(numberOfRows):
				foodNameString = checkAndExtract( tableSel, '//td/text()', i * items_per_row + 1 )
				
				if( foodNameString == "" ):
					continue
					
				foodIngredientsString = None
				
				foodPriceString = checkAndExtract( tableSel, '//td/text()', i * items_per_row + 2 )
				
				if( foodPriceString == "" ):
					continue
				
				fI = foodItem( foodNameString, categoryStrings[index], foodIngredientsString, foodPriceString )
				item['itemArray'][foodNameString] = fI
			index += 1
				
				
		return item
