from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.spiders import tesco_spider

process = CrawlerProcess(get_project_settings())
process.crawl(tesco_spider.TescoSpider)
process.start()