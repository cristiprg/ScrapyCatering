# Scrapy settings for foodCrawlers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'foodCrawlers'

SPIDER_MODULES = ['foodCrawlers.spiders']
NEWSPIDER_MODULE = 'foodCrawlers.spiders'
ITEM_PIPELINES = [ 'foodCrawlers.pipelines.FoodcrawlersPipeline', 'foodCrawlers.pipelines.XmlExportPipeline' ]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'foodCrawlers (+http://www.yourdomain.com)'
