# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from pony.orm import db_session, select, commit, desc

from .items import AnswerItem, QuestionItem, AuthorItem, CollectionAnswerItem, CollectionItem
from models.pony_models import db, Answer, Question, Author, CollectionAnswer, Collection

class ZhihuPipeline(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.db_setting = self.crawler.settings.get('DB')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        db.bind('mysql', **self.db_setting)
        db.generate_mapping()

    @db_session
    def process_item(self, item, spider):
        if isinstance(item, AnswerItem):
            answer = Answer.get(id=item['id'])
            if not answer:
                answer = Answer(**dict(item))
            elif answer.is_need_update or answer.edited_at != item['edited_at']:
                answer.summary = item['summary']
                answer.content = item['content']
                answer.vote_up = item['vote_up']
                if item.get('review_count', None):
                    answer.review_count = item['review_count']
                answer.published_at = item['published_at']
                answer.edited_at = item['edited_at']
                answer.updated_at = datetime.now()
            commit()    

        if isinstance(item, QuestionItem):
            question = Question.get(id=item['id'])
            if not question:
                question = Question(**dict(item))
            elif question.is_need_update:
                question.title = item['title']
                question.content = item['content']
                question.following_count = item['following_count']
                question.review_count = item['review_count']
                question.answer_count = item['answer_count']
                question.visit_count = item['visit_count']
                question.is_top = item['is_top']
                question.updated_at = datetime.now()
            commit()

        if isinstance(item, AuthorItem):
            author = Author.get(token=item['token'])
            # @todo: biography 和 description
            if not author:
                author = Author(**dict(item))
            elif author.is_need_update:
                author.name = item['name']
                author.biography = item['biography']
                author.pic_url = item['pic_url']
                author.description = item['description']
                author.location = item['location']
                author.visit_count = item['visit_count']
                author.business = item['business']
                author.gender = item['gender']
                author.employment = item['employment']
                author.education = item['education']
                author.follower_count = item['follower_count']
                author.followee_count = item['followee_count']
                author.thank_count = item['thank_count']
                author.aggre_count = item['aggre_count']
                author.question_count = item['question_count']
                author.answer_count = item['answer_count']
                author.post_count = item['post_count']
                author.collection_count = item['collection_count']
                author.log_count = item['log_count']
                author.visit_count = item['visit_count']
                author.updated_at = datetime.now()
            commit()

        if isinstance(item, CollectionAnswerItem):
            collection_answer = CollectionAnswer.get(collection_id=item['collection_id'], answer_id=item['answer_id'])
            if not collection_answer:
                collection_answer = CollectionAnswer(**dict(item))
                commit()

        if isinstance(item, CollectionItem):
            collection = Collection.get(id=item['id'])
            if not collection:
                collection = Collection(**dict(item))
            elif collection.is_need_update:
                collection.title = item['title']
                collection.description = item['description']
                collection.review_count = item['review_count']
            commit()

        return item