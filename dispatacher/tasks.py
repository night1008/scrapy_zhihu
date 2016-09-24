# coding: utf-8
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

import time
from celery import Celery

# from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings

from zhihu.spiders.collection import CollectionSpider
from zhihu.spiders.answer import AnswerSpider
from zhihu.spiders.question import QuestionSpider
from zhihu.spiders.author import AuthorSpider

# app = Celery('zhihu', broker="redis://localhost:6379/0", 
# 	backend='redis://localhost:6379/1')

from scrapy import crawler
from scrapy.utils.ossignal import install_shutdown_handlers
from scrapy.utils.log import configure_logging, log_scrapy_info
class CrawlerProcess(crawler.CrawlerProcess):
    # @memo: 采用此种写法打印的logger只会显示一遍，但无法写入log文件中
    def __init__(self, settings=None, install_root_handler=False):
        crawler.CrawlerRunner.__init__(self, settings)
        install_shutdown_handlers(self._signal_shutdown)
        configure_logging(self.settings, install_root_handler=install_root_handler)
        log_scrapy_info(self.settings)

app = Celery('zhihu')
app.config_from_object('config')

# @memo:启动 celery -A tasks worker --loglevel=info
# @memo: just for test
@app.task
def add(x, y):
    print 'hello celery'
    time.sleep(10)
    return x + y

@app.task(bind=True)
def collection(self, url):
    kwargs = {'url': url}
    crawler_setting = get_project_settings()
    crawler_setting.set('TASK_ID', self.request.id)
    crawler_setting.set('TASK_NAME', self.name)

    process = CrawlerProcess(crawler_setting)
    process.crawl(CollectionSpider, **kwargs)
    process.start()


@app.task(bind=True)
def answer(self, url):
    # https://github.com/scrapy/scrapy/blob/master/scrapy/settings/__init__.py
    # 'https://www.zhihu.com/question/41311028/answer/90756693'
    print '===== before spider'
    kwargs = {'url': url}
    crawler_setting = get_project_settings()
    # @memo: 加入自定义配置
    crawler_setting.set('TASK_ID', self.request.id)
    crawler_setting.set('TASK_NAME', self.name)

    process = CrawlerProcess(crawler_setting)
    process.crawl(AnswerSpider, **kwargs)
    process.start()
    print '===== after spider'

@app.task(bind=True)
def question(self, url):
    kwargs = {'url': url}
    crawler_setting = get_project_settings()
    crawler_setting.set('TASK_ID', self.request.id)
    crawler_setting.set('TASK_NAME', self.name)

    process = CrawlerProcess(crawler_setting)
    process.crawl(QuestionSpider, **kwargs)
    process.start()

@app.task(bind=True)
def author(self, url):
    kwargs = {'url': url}
    crawler_setting = get_project_settings()
    crawler_setting.set('TASK_ID', self.request.id)
    crawler_setting.set('TASK_NAME', self.name)

    process = CrawlerProcess(crawler_setting)
    process.crawl(AuthorSpider, **kwargs)
    process.start()

if __name__ == '__main__':
    from scrapy.utils.project import get_project_settings
    print get_project_settings().get('DB')
    print 'aaa'
