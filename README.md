# scrapy_zhihu
crawl zhihu using scrapy

***

```
这是在不模拟登录的情况对知乎的抓取，因此有些信息是取不到的。
想抓取自己想要的内容之后，可以进行一些操作，
比如按时间排序，按评论数排序，按内容长短排序等
```

***

# @todo:
1. sql migrate文件
2. user parse
3. falsk web app
4. 配置抽离
5. 网页模板抽离
6. celery发送任务

# 问题记录
> 自己本身在Window下开发的
1. celery启动不了，出现，`ImportError: cannot import name _uuid_generate_random`,查看
[Kombu import error on Python 2.7.11](https://github.com/celery/kombu/issues/545)
2. 启动celery需要指定队列，若是backend使用redis,则需要启动，
到对应redis目录下，先启动服务：`redis-server.exe redis.conf`