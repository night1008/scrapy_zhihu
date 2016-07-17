# conding: utf-8
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

import time
from celery import Celery

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from zhihu.spiders.answer import AnswerSpider

app = Celery('tasks', broker="redis://localhost:6379/0", 
	backend='redis://localhost:6379/1')

@app.task
def add(x, y):
    print 'hello celery'
    time.sleep(10)
    return x + y

@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def answer():    
    # crawler_setting.update({
    #     'ITEM_PIPELINES': {
    #         'dispatcher.spiders.us_keyword_research.UsKeywordResearchPipeline': 300,
    #     },
    #     'TASK_ID': self.request.id,
    #     'TASK_NAME': self.name,
    # })
    # @todo: 加入pipeline设置
    # https://github.com/scrapy/scrapy/blob/master/scrapy/settings/__init__.py
    kwargs = {'url': 'https://www.zhihu.com/question/41311028/answer/90756693'}
    crawler_setting = get_project_settings()
    process = CrawlerProcess(crawler_setting)
    process.crawl(AnswerSpider, **kwargs)
    process.start()
    

if __name__ == '__main__':
    from scrapy.utils.project import get_project_settings
    print get_project_settings().get('DB')
    print 'aaa'
