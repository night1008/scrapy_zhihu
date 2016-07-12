#coding: utf-8
from datetime import datetime
from scrapy import Spider, Request
import re
from zhihu.items import AnswerItem, QuestionItem, AuthorItem
from zhihu.utils import get_date

class AuthorSpider(Spider):
    """
    抓取知乎回答者的内容
    页面规则： 
    终端调用命令：scrapy crawl zhihu_author -a args -o zhihu_author.json
    问题：
    知乎图片获取不了
    """
    name = 'zhihu_author'
    allowed_domains = ["www.zhihu.com"]
    # start_url = 'https://www.zhihu.com/people/junlin_1980'
    start_url = 'https://www.zhihu.com/people/evanyou'

    def __init__(self, kwargs=None):
        super(AuthorSpider, self).__init__()

        # if kwargs:
        #     self.start_url = kwargs['url']
        
        self.user_token = None

    def start_requests(self):
        m = re.search('\/people\/(.+)', self.start_url)
        if not m:
            self.logger.error('============>')
            self.logger.error('Parse no author token')
            return
        self.user_token = m.groups()[0]

        return [Request(self.start_url, callback=self.parse)]

    def parse(self, response):              
        author_name = response.css('div.zm-profile-header div.title-section span.name::text').extract_first()
        author_biography = response.css('div.zm-profile-header div.title-section span.bio::attr(title)').extract_first()
        author_pic_url = response.css('img.Avatar::attr(src)').extract_first()
        author_description = response.css('div.zm-profile-header-description span.description span.content').re('<span.*?>([\S\s]+)<\/span>')
        author_location = response.css('span.item.location::attr(title)').extract_first()
        author_business = response.css('span.item.business::attr(title)').extract_first()
        
        # @memo: 解析性别
        author_gender_class = response.css('span.gender.item i::attr(class)').extract_first()
        if 'female' in author_gender_class:
            author_gender = 0
        elif 'male' in author_gender_class:
            author_gender = 1
        else:
            author_gender = None

        author_employment = response.css('span.item.employment::attr(title)').extract_first()
        author_education = response.css('span.item.education::attr(title)').extract_first()
        author_follower_count = response.css('div.zm-profile-side-following a.item[href*=followers] strong::text').extract_first()
        author_followee_count = response.css('div.zm-profile-side-following a.item[href*=followees] strong::text').extract_first()
        author_thank_count = response.css('div.zm-profile-header-info-list span.zm-profile-header-author-thanks strong::text').extract_first()
        author_aggre_count = response.css('div.zm-profile-header-info-list span.zm-profile-header-author-agree strong::text').extract_first()
        author_question_count = response.css('div.profile-navbar a.item[href*=asks] span.num::text').extract_first()
        author_answer_count = response.css('div.profile-navbar a.item[href*=answers] span.num::text').extract_first()
        author_post_count = response.css('div.profile-navbar a.item[href*=posts] span.num::text').extract_first()
        author_collection_count = response.css('div.profile-navbar a.item[href*=collections] span.num::text').extract_first()
        author_log_count = response.css('div.profile-navbar a.item[href*=logs] span.num::text').extract_first()
        author_visit_count = response.css('div.zm-profile-side-section span.zg-gray-normal strong::text').extract_first()

        author_item = AuthorItem()
        author_item['token'] = self.user_token
        author_item['name'] = author_name
        author_item['biography'] = author_biography
        author_item['pic_url'] = author_pic_url
        author_item['description'] = author_description
        author_item['location'] = author_location
        author_item['business'] = author_business
        author_item['gender'] = author_gender
        author_item['employment'] = author_employment
        author_item['education'] = author_education
        author_item['follower_count'] = author_follower_count
        author_item['followee_count'] = author_followee_count
        author_item['thank_count'] = author_thank_count
        author_item['aggre_count'] = author_aggre_count
        author_item['question_count'] = author_question_count
        author_item['answer_count'] = author_answer_count
        author_item['post_count'] = author_post_count
        author_item['collection_count'] = author_collection_count
        author_item['log_count'] = author_log_count
        author_item['visit_count'] = author_visit_count

        self.logger.info(author_item)
        yield author_item

        question_uris = response.css('div#zh-profile-ask-wrap div#zh-profile-ask-inner-list h2.zm-profile-question a.question_link::attr(href)').extract()
        for question_uri in question_uris:
            question_url = response.urljoin(question_uri)
            yield Request(question_url,
                    callback=self.parse_question)

    def parse_question(self, response):
        question_user_token = self.user_token

        question_id = re.search('question/(\d{8})', response.url).groups()[0]
        question_title = response.css('div#zh-question-title h2.zm-item-title span.zm-editable-content').re_first(
            '<span.*?>([\S\s]+)<\/span>').replace("\n", "")
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
        question_item['id'] = question_id
        question_item['user_token'] = question_user_token
        question_item['title'] = question_title
        question_item['content'] = question_content
        question_item['following_count'] = question_following_count
        question_item['review_count'] = question_review_count
        question_item['answer_count'] = question_answer_count
        question_item['is_top'] = question_is_top == 'true'
        question_item['visit_count'] = question_visit_count

        yield question_item