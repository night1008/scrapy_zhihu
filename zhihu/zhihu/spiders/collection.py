#coding: utf-8
from datetime import datetime
from scrapy import Spider, Request
import re
from zhihu.items import AnswerItem, QuestionItem
from zhihu.utils import get_date

class CollectionSpider(Spider):
    """
    抓取知乎收藏的内容
    页面规则： 
    终端调用命令：scrapy crawl zhihu_collection -a args -o zhihu_collection.json
    问题：
    知乎图片获取不了
    """
    name = 'zhihu_collection'
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/collection/25185328']
    count = 0

    # def start_requests(self):
    #     return [Request("https://www.zhihu.com/login", meta = {'cookiejar' : 1}, callback = self.post_login)]

    # #FormRequeset出问题了
    # def post_login(self, response):
    #     print 'Preparing login'
    #     #下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
    #     xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
    #     print xsrf
    #     #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
    #     #登陆成功后, 会调用after_login回调函数
    #     return [FormRequest.from_response(response,   #"http://www.zhihu.com/login",
    #                         meta = {'cookiejar' : response.meta['cookiejar']},
    #                         headers = self.headers,  #注意此处的headers
    #                         formdata = {
    #                         '_xsrf': xsrf,
    #                         'email': '1179039379@qq.com',
    #                         'password': '123456'
    #                         },
    #                         callback = self.after_login,
    #                         dont_filter = True
    #                         )]

    # def after_login(self, response) :
    #     for url in self.start_urls :
    #         yield self.make_requests_from_url(url)

    def parse(self, response):
        self.logger.info('parse')
        answer_divs = response.css('div#zh-list-answer-wrap div.zm-item')
        # with open('res.html', 'wb') as f:
        #     f.write(response.body)

        self.logger.info(len(answer_divs))

        for index, answer_div in enumerate(answer_divs):
            # @todo:问题
            question_url_str = answer_div.css('h2.zm-item-title a::attr("href")').extract_first()
            answer_url_str = answer_div.css('div.zm-item-answer div.zm-item-rich-text::attr("data-entry-url")').extract_first()
            self.logger.info('===>' + str(index))

            # self.count += 1
            # if self.count > 2:
            #     break
            if question_url_str:
                question_url = response.urljoin(question_url_str)
                self.logger.info(question_url)
                yield Request(question_url, 
                    # meta={'cookiejar': response.meta['cookiejar']},
                    callback=self.parse_question)

            if answer_url_str:
                answer_url = response.urljoin(answer_url_str)
                answer_review_count = answer_div.css('a.toggle-comment[name*=addcomment]::text').re_first('(\d+)')
                if not answer_review_count:
                    answer_review_count = 0
                #todo: 传递review_count到answer_url
                yield Request(answer_url, 
                    # meta={'cookiejar': response.meta['cookiejar']},
                    meta={'review_count': answer_review_count},
                    callback=self.parse_answer)
            else:
                answer_status_divs = answer_div.css('div.answer-status')
                if len(answer_status_divs):
                    self.logger.warning('可能涉及违反法律法规的内容')
        
    def parse_answer(self, response):
        self.logger.info('parse_answer')
        self.logger.info(response.url)
        
        question_id, answer_id = re.search('question/(\d{8})/answer/(\d{8})', response.url).groups()
        answer_div = response.css('div#zh-question-answer-wrap')        
        answer_content = answer_div.css('div.zm-editable-content').re_first('<div.*?>([\S\s]+)<\/div>')
        answer_vote_up = answer_div.css('div.zm-votebar button.up span.count::text').extract_first().replace('K', '000').replace('W', '0000')
        answer_user_token = answer_div.css('a.author-link::attr(href)').re_first('\/people\/(.*)')
        answer_published_at_str = answer_div.css('a.answer-date-link::attr(data-tip)').extract_first()
        answer_edited_at = None
        # s$t$发布于 昨天 08:03 编辑于 昨天 11:55
        if not answer_published_at_str:
            answer_published_at_str = answer_div.css('a.answer-date-link::text').extract_first()
            answer_published_at = get_date(answer_published_at_str)
        else:
            answer_published_at = get_date(answer_published_at_str)
            answer_edited_at_str = answer_div.css('a.answer-date-link::text').extract_first()
            answer_edited_at = get_date(answer_edited_at_str)

        answer_item = AnswerItem()
        answer_item['id'] = answer_id
        answer_item['user_token'] = answer_user_token
        answer_item['question_id'] = question_id
        answer_item['content'] = answer_content
        answer_item['content_length'] = len(answer_content) if answer_content else 0
        answer_item['vote_up'] = answer_vote_up
        answer_item['vote_down'] = None
        answer_item['review_count'] = response.meta.get('review_count')
        answer_item['published_at'] = answer_published_at
        answer_item['edited_at'] = answer_edited_at

        yield answer_item

    def parse_question(self, response):
        question_id = re.search('question/(\d{8})', response.url).groups()[0]
        question_title = response.css('div#zh-question-title h2.zm-item-title.zm-editable-content').re_first('<h2.*?>([\S\s]+)<\/h2>').replace("\n", "")
        question_content = response.css('div#zh-question-detail div.zm-editable-content').re_first('<div.*?>([\S\s]+)<\/div>')
        question_following_count_str = response.css('div#zh-question-side-header-wrap::text').extract()
        question_following_count = question_following_count_str[1].strip().split('\n')[0].replace(',', '')
        question_review_count = response.css('a.toggle-comment[name*=addcomment]::text').re_first('([0-9,]+)').replace(',', '')
        question_answer_count = response.css('h3#zh-question-answer-num::attr(data-num)').extract_first()
        question_is_top = response.css('div.zu-main-content meta[itemprop*=isTopQuestion]::attr(content)').extract_first()
        question_visit_count = response.css('div.zu-main-content meta[itemprop*=visitsCount]::attr(content)').extract_first()

        question_item = QuestionItem()
        question_item['id'] = question_id
        question_item['title'] = question_title
        question_item['content'] = question_content
        question_item['following_count'] = question_following_count
        question_item['review_count'] = question_review_count
        question_item['answer_count'] = question_answer_count
        question_item['is_top'] = question_is_top == 'true'
        question_item['visit_count'] = question_visit_count

        yield question_item
