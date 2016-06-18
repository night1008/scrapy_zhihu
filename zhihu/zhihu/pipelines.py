# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from zhihu.items import AnswerItem, QuestionItem, AuthorItem, CollectionAnswerItem, CollectionItem
from models import Session, Answer, Question, Author, CollectionAnswer, Collection

class ZhihuPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AnswerItem):
            session = Session()
            answer = session.query(Answer).filter_by(id=item['id']).first()
            if not answer:
                answer = Answer(**dict(item))
                session.add(answer)
            elif answer.edited_at and answer.edited_at != item['edited_at']:
                answer.summary = item['summary']
                answer.content = item['content']
                answer.vote_up = item['vote_up']
                answer.review_count = item['review_count']
                answer.published_at = item['published_at']
                answer.edited_at = item['edited_at']
                answer.updated_at = datetime.now()
            elif answer.is_need_update():
                answer.vote_up = item['vote_up']
                answer.review_count = item['review_count']
                answer.updated_at = datetime.now()
            session.commit()
            session.close()

        if isinstance(item, QuestionItem):
            session = Session()
            question = session.query(Question).filter_by(id=item['id']).first()
            if not question:
                question = Question(**dict(item))
                session.add(question)
            elif question.is_need_update():
                question.title = item['title']
                question.content = item['content']
                question.following_count = item['following_count']
                question.review_count = item['review_count']
                question.answer_count = item['answer_count']
                question.visit_count = item['visit_count']
                question.is_top = item['is_top']
                question.updated_at = datetime.now()
            session.commit()
            session.close()

        if isinstance(item, AuthorItem):
            session = Session()
            author = session.query(Author).filter_by(token=item['token']).first()
            if not author:
                author = Author(**dict(item))
                session.add(author)
            elif author.is_need_update():
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
            session.commit()
            session.close()

        if isinstance(item, CollectionAnswerItem):
            session = Session()
            collection_answer = session.query(CollectionAnswer).filter_by(
                collection_id=item['collection_id'], answer_id=item['answer_id']).first()
            if not collection_answer:
                collection_answer = CollectionAnswer(**dict(item))
                session.add(collection_answer)
                session.commit()
                session.close()

        if isinstance(item, CollectionItem):
            session = Session()
            collection = session.query(Collection).filter_by(id=item['id']).first()
            if not collection:
                collection = Collection(**dict(item))
                session.add(collection)
            elif collection.is_need_update():
                collection.title = item['title']
                collection.description = item['description']
                collection.review_count = item['review_count']
            session.commit()
            session.close()

        return item
