# coding: utf-8

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from zhihu.spiders.answer import AnswerSpider
from zhihu.spiders.author import AuthorSpider
from zhihu.spiders.question import QuestionSpider

if __name__ == "__main__":

	process = CrawlerProcess(get_project_settings())
	process.crawl(QuestionSpider)
	process.start() 
