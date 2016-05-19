# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from zhihu.items import AnswerItem, QuestionItem, UserItem, CollectionAnswerItem
from models import Session, Answer, Question, User, CollectionAnswer

class ZhihuPipeline(object):
    def process_item(self, item, spider):
    	if isinstance(item, AnswerItem):
            session = Session()
            answer = session.query(Answer).filter_by(id=item['id']).first()
            if not answer:
                answer = Answer(**dict(item))
                session.add(answer)
            elif answer.edited_at and answer.edited_at != item['edited_at']:
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
            spider.logger.error(question)
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

        if isinstance(item, UserItem):
            session = Session()
            user = session.query(User).filter_by(token=item['token']).first()
            if not user:
                user = User(**dict(item))
                session.add(user)
            elif user.is_need_update():
                user.name = item['name']
                user.biography = item['biography']
                user.pic_url = item['pic_url']
                user.description = item['description']
                user.location = item['location']
                user.visit_count = item['visit_count']
                user.business = item['business']
                user.gender = item['gender']
                user.employment = item['employment']
                user.education = item['education']
                user.follower_count = item['follower_count']
                user.followee_count = item['followee_count']
                user.thank_count = item['thank_count']
                user.aggre_count = item['aggre_count']
                user.question_count = item['question_count']
                user.answer_count = item['answer_count']
                user.post_count = item['post_count']
                user.collection_count = item['collection_count']
                user.log_count = item['log_count']
                user.visit_count = item['visit_count']
                user.updated_at = datetime.now()
            session.commit()
            session.close()

        if isinstance(item, CollectionAnswerItem):
            session = Session()
            collection_answer = session.query(CollectionAnswer).filter_by( \
                collection_id=item['collection_id'], answer_id=item['answer_id']).first()
            if not collection_answer:
                collection_answer = CollectionAnswer(**dict(item))
                session.add(collection_answer)
                session.commit()
                session.close()
            
        return item
