from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from foodCrawlers.items import FoodcrawlersItem
from foodCrawlers.checker import checkAndExtract
from foodCrawlers.foodItem import foodItem

import string
import unicodedata

class PickleBarrelCatering(CrawlSpider):
	name = 'pickleBarrelCatering'
	allowed_domains = ['picklebarrelcatering.com']
	start_urls = ['http://picklebarrelcatering.com']

	# The rules which to apply when parsing a site
	rules = ( 
		Rule(SgmlLinkExtractor(allow=(".*/catering-menu/[^/]*html"),deny=("\?") ), callback='parse_item', follow=True),
	)
	
	def parse_item( self, response ):
		print "Hello"
		hxs = HtmlXPathSelector( response )
		item = FoodcrawlersItem()
		item['itemArray'] = {}
		
		# The category is the last part of the URL without the ".html"
		category = string.split( string.split( response.url, '/' )[-1], '.' )[0]
		
		paragraphs = hxs.select('//ol[@id="products-list"]//li').extract()
		
		# We crawl the sites paragraph by paragraph because in a paragraph
		# we will have the food name, ingredients and price grouped
		for paragraph in paragraphs:
			paragraphSelector = HtmlXPathSelector( text = paragraph )
			foodNameString = checkAndExtract( paragraphSelector, '//h2//a/text()' )
			
			# If we get an empty string then we skip this item
			if( foodNameString == "" ):
				continue
				
			foodIngredientsString = checkAndExtract( paragraphSelector, '//div[@class="desc std"]/text()' )
			# It is possible the format is different on some pages
			if( foodIngredientsString == "" ):
				foodIngredientsParas = checkAndExtract( paragraphSelector, '//div[@class="desc std"]' )
	
				foodHxs = HtmlXPathSelector( text = foodIngredientsParas )
				result = foodHxs.select( '//p/text()' ).extract()
				for foodIng in result:
					foodIngredientsString += foodIng
				
			
			foodPriceString = checkAndExtract( paragraphSelector, '//span[@class="price"]/text()' )
			
			fI = foodItem( foodNameString, category, foodIngredientsString, foodPriceString )
			item['itemArray'][foodNameString] = fI
			
		
		
		return item
