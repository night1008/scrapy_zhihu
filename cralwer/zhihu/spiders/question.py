#coding: utf-8
import re

from scrapy import Spider, Request

from ..items import AnswerItem, QuestionItem
from ..utils import get_date

class QuestionSpider(Spider):
    """
    抓取知乎收藏的内容
    页面规则： 
    终端调用命令：scrapy crawl zhihu_question -a args -o zhihu_question.json
    问题：
    知乎图片获取不了
    ?sort=created 可以按时间排序
    """
    name = 'zhihu_question'
    allowed_domains = ["www.zhihu.com"]
    # start_urls = ['https://www.zhihu.com/question/40170848']

    def __init__(self, url=None):
        super(QuestionSpider, self).__init__()

        self.url = url

    def start_requests(self):
        yield Request(self.url, self.parse)

    def parse(self, response):
        m = re.search('question/(\d{8,})', response.url)
        
        if not m:
            self.logger.error('=============>')
            self.logger.error(response.url)
            return

        self.question_id = m.groups()[0]

        question_title = response.css('div#zh-question-title h2.zm-item-title span.zm-editable-content') \
                                .re_first('<span.*?>([\S\s]+)<\/span>').replace("\n", "")
        question_content = response.css('div#zh-question-detail div.zm-editable-content').re_first('<div.*?>([\S\s]+)<\/div>')
        question_following_count_str = response.css('div#zh-question-side-header-wrap::text').extract()
        question_following_count = question_following_count_str[1].strip().split('\n')[0].replace(',', '')
        question_review_count = response.css('a.toggle-comment[name*=addcomment]::text').re_first('([0-9,]+)')

        if not question_review_count:
            question_review_count = 0
        else:
            question_review_count = question_review_count.replace(',', '')
            
        question_answer_count = response.css('h3#zh-question-answer-num::attr(data-num)').extract_first()
        question_is_top = response.css('div.zu-main-content meta[itemprop*=isTopQuestion]::attr(content)').extract_first()
        question_visit_count = response.css('div.zu-main-content meta[itemprop*=visitsCount]::attr(content)').extract_first()

        question_item = QuestionItem()
        question_item['id'] = self.question_id
        question_item['user_token'] = None
        question_item['title'] = question_title
        question_item['content'] = question_content
        question_item['following_count'] = question_following_count
        question_item['review_count'] = question_review_count
        question_item['answer_count'] = question_answer_count
        question_item['is_top'] = question_is_top == 'true'
        question_item['visit_count'] = question_visit_count

        yield question_item

        answer_divs = response.css('div#zh-question-answer-wrap div.zm-item-answer')

        for index, answer_div in enumerate(answer_divs):
            answer_url_str = answer_div.css('link[itemprop*=url]::attr(href)').extract_first()

            if answer_url_str:
                answer_url = response.urljoin(answer_url_str)
                answer_review_count = answer_div.css('a.toggle-comment[name*=addcomment]::text').re_first('(\d+)')
                if not answer_review_count:
                    answer_review_count = 0
                    
                yield Request(answer_url, 
                    meta={'review_count': answer_review_count},
                    callback=self.parse_answer)
            else:
                answer_status_divs = answer_div.css('div.answer-status')
                if len(answer_status_divs):
                    self.logger.warning('可能涉及违反法律法规的内容')
        
    def parse_answer(self, response):
        m = re.search('question/(\d{8,})/answer/(\d{8,})', response.url)
        
        if not m:
            self.logger.error('=============>')
            self.logger.error(response.url)
            return

        question_id, answer_id = m.groups()
        answer_div = response.css('div#zh-question-answer-wrap')
        answer_summary_element = answer_div.css('div.zh-summary.summary')
        answer_summary = answer_summary_element.re_first('<div.*?>([\S\s]+)\s*?<a.*?>.*<\/a>\s*<\/div>')
        if not answer_summary:
            answer_summary = answer_summary_element.re_first('<div.*?>([\S\s]+)<\/div>')
        answer_content = answer_div.css('div.zm-editable-content').re_first('<div.*?>([\S\s]+)<\/div>')
        answer_vote_up = answer_div.css('div.zm-votebar button.up span.count::text').extract_first().replace('K',
                                                                                                             '000').replace(
            'W', '0000')
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
        answer_item['summary'] = answer_summary
        answer_item['content'] = answer_content
        answer_item['vote_up'] = answer_vote_up
        answer_item['vote_down'] = None
        answer_item['review_count'] = response.meta.get('review_count')
        answer_item['published_at'] = answer_published_at
        answer_item['edited_at'] = answer_edited_at
        yield answer_item
