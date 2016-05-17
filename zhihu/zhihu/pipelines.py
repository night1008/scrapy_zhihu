# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from zhihu.items import AnswerItem, QuestionItem, UserItem
from models import Session, Answer, Question, User

class ZhihuPipeline(object):
    def process_item(self, item, spider):
    	if isinstance(item, AnswerItem):
            session = Session()
            answer = session.query(Answer).filter_by(id=item['id']).first()
            if not answer:
                answer = Answer(**dict(item))
                session.add(answer)
                session.commit()
                session.close()
                # @todo:更新机制
    	
        if isinstance(item, QuestionItem):
            session = Session()
            question = session.query(Question).filter_by(id=item['id']).first()
            spider.logger.error(question)
            if not question:
                question = Question(**dict(item))
                session.add(question)
                session.commit()
                session.close()
            # @todo:更新机制

        if isinstance(item, UserItem):
            session = Session()
            user = session.question(User).filter_by(token=item['token']).first()
            if not user:
                user = User(**dict(item))
                session.add(user)
                session.commit()
                session.close()
            
        return item
