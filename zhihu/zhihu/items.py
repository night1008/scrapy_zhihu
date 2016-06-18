# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AnswerItem(scrapy.Item):
    id = scrapy.Field()
    user_token = scrapy.Field()
    question_id = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    review_count = scrapy.Field()
    vote_up = scrapy.Field()
    vote_down = scrapy.Field()
    published_at = scrapy.Field()
    edited_at = scrapy.Field()

class QuestionItem(scrapy.Item):
    id = scrapy.Field()
    user_token = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    following_count = scrapy.Field()
    review_count = scrapy.Field()
    answer_count = scrapy.Field()
    visit_count = scrapy.Field()
    is_top = scrapy.Field()

class AuthorItem(scrapy.Item):
    token = scrapy.Field()
    gender = scrapy.Field()
    pic_url = scrapy.Field()
    description = scrapy.Field()
    location = scrapy.Field()
    name = scrapy.Field()
    biography = scrapy.Field()
    business = scrapy.Field()
    employment =scrapy.Field()
    education = scrapy.Field()
    follower_count = scrapy.Field()
    followee_count = scrapy.Field()
    question_count = scrapy.Field()
    answer_count = scrapy.Field()
    collection_count = scrapy.Field()
    post_count = scrapy.Field()
    log_count = scrapy.Field()
    aggre_count = scrapy.Field()
    thank_count = scrapy.Field()
    visit_count = scrapy.Field()

class CollectionItem(scrapy.Item):
    id = scrapy.Field()
    user_token = scrapy.Field()
    title = scrapy.Field()
    review_count = scrapy.Field()
    description = scrapy.Field()

class CollectionAnswerItem(scrapy.Item):
    collection_id = scrapy.Field()
    answer_id = scrapy.Field()
