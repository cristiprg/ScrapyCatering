from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from foodCrawlers.items import FoodcrawlersItem
import string
from foodCrawlers.foodItem import foodItem
import os
import unicodedata
from scrapy.item import Item, Field

class AllspicecateringSpider(CrawlSpider):
	name = 'allSpiceCatering'
	allowed_domains = ['allspicecatering.com']
	start_urls = ['http://www.allspicecatering.com/']

	rules = (
		Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		item = FoodcrawlersItem()
		item['stuff'] = {}
		category = string.split(string.split(response.url, '/')[-1], '.')[0] #the last part of the url, without ".html"\
		
		#extract the whole paragraph which contains all the information grouped: title, ingredients, price
		#previously @id="colbody1"
		paragraphs = hxs.select('//div[@class="blockbody"]//p').extract()
		
		#for each paragraph, extract the foodItem
		foodItemArray = []
		for paragraph in paragraphs:
			paragraphSelector = HtmlXPathSelector(text=paragraph)
			foodName = paragraphSelector.select('//p/font[@size="4"]/text()').extract()
			
			# if there is no proper food title we skip this item 
			if foodName == []:
				continue
				
			foodNameUnicode = foodName[0].replace( '\r\n', '' )
			foodNameString = unicodedata.normalize( 'NFKD', foodNameUnicode ).encode( 'ascii', 'ignore' )
			
			# if we get an empty string we skip this item
			if( foodNameString == "" ):
				continue
			
			#TODO1: consult the ontology to determine whether foodNameString is valid or not
			
			foodIngredientsAndPrice = paragraphSelector.select( '//p/text()')
			
			#select food ingredients
			foodIngredients = foodIngredientsAndPrice.extract()
			if foodIngredients == []:
				continue			
			foodIngredientsUnicode = foodIngredients[0].replace( '\r\n', '' )
			foodIngredientsString = unicodedata.normalize( 'NFKD', foodIngredientsUnicode ).encode( 'ascii', 'ignore' )
			
			
			#TODO1: consult the ontology to determine whether foodIngredientsString is valid or not
			
			#select food price
			foodPrice = foodIngredientsAndPrice.re('\$[-+]?[0-9]*\.?[0-9]+$')
			if foodPrice == []:
				continue
			foodPriceUnicode = foodPrice[0]
			foodPriceString = unicodedata.normalize( 'NFKD', foodPriceUnicode ).encode( 'ascii', 'ignore' )
			
			
			
			
			fI = foodItem(foodNameString, category, foodIngredientsString, foodPriceString)
			foodItemArray.append(fI)
			
			#TODO2: find a way to pass fI to item pipeline

			item['stuff'][foodNameString] = fI
			
			#fI.display()
			
			#print "---", "Food ingredients: ", foodIngredientsAndPrice[0]
			
					
		
		return item
		
