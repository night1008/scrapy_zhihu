#coding: utf-8
from scrapy import Spider, Request
import re
from zhihu.items import AnswerItem

class QuestionSpider(Spider):
    """
    抓取知乎收藏的内容
    页面规则： 
    终端调用命令：scrapy crawl zhihu_question -a args -o zhihu_question.json
    问题：
    知乎图片获取不了
    """
    name = 'zhihu_question'
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/question/40170848']

    def parse(self, response):
        
        question_title = response.css('div#zh-question-title h2.zm-item-title.zm-editable-content').re_first('<h2.*?>([\S\s]+)<\/h2>')
        question_content = response.css('div#zh-question-detail div.zm-editable-content').re_first('<div.*?>([\S\s]+)<\/div>')
        question_following_count_str = response.css('div#zh-question-side-header-wrap::text').extract()
        question_following_count = question_following_count_str[1].strip().split('\n')[0].replace(',', '')
        question_review_count = response.css('a.toggle-comment[name*=addcomment]::text').re_first('([0-9,]+)').replace(',', '')
        question_answer_count = response.css('h3#zh-question-answer-num::attr(data-num)').extract_first()
        question_is_top = response.css('div.zu-main-content meta[itemprop*=isTopQuestion]::attr(content)').extract_first()
        question_visit_count = response.css('div.zu-main-content meta[itemprop*=visitsCount]::attr(content)').extract_first()

        # question_topic_ids = 
        
        question_item = {
            'title': question_title,
            'content': question_content,
            'following_count': question_following_count,
            'review_count': question_review_count,
            'answer_count': question_answer_count,
            'is_top': question_is_top,
            'visit_ount': question_visit_count,
        }

        yield question_item
        return

        answer_divs = response.css('div#zh-list-answer-wrap div.zm-item')
        # with open('res.html', 'wb') as f:
        #     f.write(response.body)

        self.logger.info(len(answer_divs))

        for index, answer_div in enumerate(answer_divs):
            # @todo:问题
            question_url_str = answer_div.css('h2.zm-item-title a::attr("href")').extract_first()
            answer_url_str = answer_div.css('div.zm-item-answer div.zm-item-rich-text::attr("data-entry-url")').extract_first()
            self.logger.info('============' + str(index))

            if question_url_str:
                question_url = response.urljoin(question_url_str)
                self.logger.info(question_url)
                yield Request(question_url, 
                    # meta={'cookiejar': response.meta['cookiejar']},
                    callback=self.parse_question)

            if answer_url_str:
                answer_url = response.urljoin(answer_url_str)
                self.logger.info(answer_url)
                yield Request(answer_url, 
                    # meta={'cookiejar': response.meta['cookiejar']},
                    callback=self.parse_answer)
            else:
                answer_status_divs = answer_div.css('div.answer-status')
                if len(answer_status_divs):
                    self.logger.warning('可能涉及违反法律法规的内容')
        
    def parse_answer(self, response):
        self.logger.info('parse_answer')
        self.logger.info(response.url)
        # with open('answer_res.html', 'wb') as f:
        #     f.write(response.body)
        # return
        question_id, answer_id = re.search('question/(\d{8})/answer/(\d{8})', response.url).groups()
        answer_div = response.css('div#zh-question-answer-wrap')        
        answer_content = answer_div.css('div.zm-editable-content').re_first('<div.*?>([\S\s]+)<\/div>')
        answer_vote_up = answer_div.css('div.zm-votebar button.up span.count::text').extract_first()

        answer_item = AnswerItem()
        answer_item['id'] = answer_id
        answer_item['question_id'] = question_id
        answer_item['content'] = answer_content
        answer_item['vote_up'] = answer_vote_up
        answer_item['vote_down'] = None

        yield answer_item
