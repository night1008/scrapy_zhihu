# coding: utf-8

from app.app import app
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from zhihu.spiders.answer import AnswerSpider

if __name__ == "__main__":

    app.run()
	# process = CrawlerProcess(get_project_settings())
	# process.crawl(AnswerSpider)
	# process.start() 
