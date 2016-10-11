# -*- coding: utf-8 -*-
from .web_config import DB

SCRAPY = {
    'DB': DB,
    'BOT_NAME': 'zhihu',
    # 'SPIDER_MODULES': ['zhihu.spiders'],
    # 'NEWSPIDER_MODULE': 'zhihu.spiders',
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'DOWNLOAD_DELAY': 1,
    'COOKIES_ENABLED': True,
    'COOKIES_DEBUG': True,
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'http://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    },
    'LOG_LEVEL': 'INFO',
    'ITEM_PIPELINES': {
        'cralwer.zhihu.pipelines.ZhihuPipeline': 300,
    },
    'EXTENSIONS': {
    },
    'DOWNLOADER_MIDDLEWARES': {
    },
    'CONCURRENT_REQUESTS': 32,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
    'AUTOTHROTTLE_ENABLED': False,
    'DOWNLOAD_TIMEOUT': 200,  # @todo: 为什么

    # 不需要用到的 scrpay middleware
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,       # @memo: 没有用到用到认证的请求
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,     # @memo: Crawlera已包含
}