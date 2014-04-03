from spiderHeader import *

class ThecapitalgrilleSpider(CrawlSpider):
	name = 'thecapitalgrille'
	allowed_domains = ['thecapitalgrille.com']
	start_urls = ['http://www.thecapitalgrille.com/']

	rules = (
		Rule(SgmlLinkExtractor( allow=(".*/menu/.*") ), callback='parse_item', follow=True), #allow more
	)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		item = FoodcrawlersItem()
		item['itemArray'] = {}
		
		#extract the whole paragraph which contains all food names and that description which we'll consider ingredients
		paragraphs = hxs.select('//ul[@class="appetizers"]/li').extract()
		
		for paragraph in paragraphs:
			paragraphSelector = HtmlXPathSelector(text=paragraph)
			
			foodNameString = checkAndExtract( paragraphSelector, '//h4/text()' )
			if foodNameString == "" :
				continue		
			
			ingredientsString = checkAndExtract( paragraphSelector, '//p/text()' )
			if ingredientsString == "" :
				continue
			
			fI = foodItem(foodName=foodNameString, ingredients=ingredientsString, category=None, price=None)
			item['itemArray'][foodNameString] = fI
			
		return item
"""		
		#for each paragraph, extract the foodItem
		foodItemArray = []
		for paragraph in paragraphs:
			paragraphSelector = HtmlXPathSelector(text=paragraph)

			foodNameString = checkAndExtract( paragraphSelector, '//p/font[@size="4"]/text()' )

			# if we get an empty string we skip this item
			if( foodNameString == "" ):
				continue			

			#select food ingredients
			foodIngredientsString = checkAndExtract( paragraphSelector, '//p/text()' )
			
			
			
			#TODO1: consult the ontology to determine whether foodIngredientsString is valid or not
			
			#select food price
			foodIngredientsAndPrice = paragraphSelector.select( '//p/text()')
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
			
"""
		

		
