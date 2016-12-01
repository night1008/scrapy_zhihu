# coding: utf-8

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from cralwer.zhihu.spiders.answer import AnswerSpider
from cralwer.zhihu.spiders.author import AuthorSpider
from cralwer.zhihu.spiders.question import QuestionSpider
from config import scrapy_config

if __name__ == "__main__":
	crawler_setting = scrapy_config.SCRAPY

    # crawler_setting.update({
    #     'ITEM_PIPELINES': {
    #         'dispatcher.spiders.us_keyword_digging.UsKeywordDiggingPipeline': 300,
    #     },
    #     'TASK_ID': self.request.id,
    #     'TASK_NAME': self.name,
    # })

	print crawler_setting.get('DB')
	print crawler_setting.get('BOT_NAME')

	process = CrawlerProcess(crawler_setting)
	process.crawl(AnswerSpider, url='https://pic2.zhimg.com/v2-113ddad0903626ce2615ffe2af43d069_r.png')
	process.start()
