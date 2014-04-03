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
