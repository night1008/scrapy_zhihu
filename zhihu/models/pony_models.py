# coding: utf-8

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from pony.orm import *
from flask.ext.login import UserMixin

db = Database()

class User(db.Entity, UserMixin):
    _table_ = 'user'

    id = PrimaryKey(int, unsigned=True, auto=True)
    name = Optional(str)
    email = Required(str)
    password = Required(str)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    @classmethod
    def set_password(cls, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)  

class Answer(db.Entity):
    _table_ = 'answer'

    UPDATE_DAY = 5
    PER_PAGE = 10

    id = PrimaryKey(int)
    user_token = Optional(str)
    question_id = Required(str)
    summary = Required(LongStr)
    content = Optional(LongStr)
    vote_up = Required(int)
    vote_down = Optional(int)  
    review_count = Optional(int)  
    published_at = Optional(datetime)
    edited_at = Optional(datetime)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)

    @property
    def is_need_update(self):
        return self.updated_at + timedelta(days=self.UPDATE_DAY) > datetime.now()

    @db_session
    def question(self):
        return Question.get(id=self.question_id)

class Question(db.Entity):
    _table_ = 'question'

    UPDATE_DAY = 5
    PER_PAGE = 10

    id = PrimaryKey(int)
    user_token = Optional(str)
    title = Required(str)
    content = Optional(LongStr)
    following_count = Required(int)
    review_count = Required(int)
    answer_count = Required(int)
    visit_count = Required(int)
    is_top = Optional(bool, default=False)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)

    # answers = Set('Answer', table="Answer", column='answer_id')
    @property
    def is_need_update(self):
        return self.updated_at + timedelta(days=self.UPDATE_DAY) > datetime.now()

    @db_session
    def answers(self, offset=None, limit=None):
        answers_query = select(a for a in Answer if a.question_id == self.id)
        if offset is not None and limit:
            answers = answers_query.limit(offset, limit)
        else:
            answers = answers_query[:]
        return answers

class Collection(db.Entity):
    _table_ = 'collection'

    UPDATE_DAY = 10
    PER_PAGE = 10

    id = PrimaryKey(int)
    user_token = Optional(str)
    title = Required(str)
    description = Optional(LongStr)
    review_count = Optional(int)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)

    @property
    def is_need_update(self):
        return self.updated_at + timedelta(days=self.UPDATE_DAY) > datetime.now()  

class CollectionAnswer(db.Entity):
    _table_ = 'collection_answer'

    id = PrimaryKey(int)
    collection_id = Required(int)
    answer_id = Required(int)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)

class Author(db.Entity):
    _table_ = 'author'

    UPDATE_DAY = 5
    PER_PAGE = 10

    id = PrimaryKey(int)
    token = Optional(str)
    name = Required(str)
    biography = Optional(str)
    pic_url = Optional(str)
    description = Optional(LongStr)
    location = Optional(str)
    business = Optional(str)
    gender = Required(int)
    employment = Optional(str)
    education = Optional(str)
    follower_count = Optional(int)
    followee_count = Optional(int)
    thank_count = Optional(int)
    aggre_count = Optional(int)
    question_count = Optional(int)
    answer_count = Optional(int)
    post_count = Optional(int)
    collection_count = Optional(int)
    log_count = Optional(int)
    visit_count = Optional(int)
    created_at = Required(datetime, default=datetime.now)
    updated_at = Required(datetime, default=datetime.now)

    @property
    def is_need_update(self):
        return self.updated_at + timedelta(days=self.UPDATE_DAY) > datetime.now()


if __name__ == '__main__':

    # @todo: 测试
    from pony.orm import db_session

    # import config

    DB = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '100815',
        'db': 'zhihu',
    }

    # @test: 1
    db.bind('mysql', **DB)
    db.generate_mapping()

    with db_session:
        # u1 = User(name='John', email='111@qq.com', password='aa')
        a1 = select(a for a in Answer).first()
        a2 = select(a.id for a in Answer)[:10]

        q1 = select(q for q in Question).first()

    from IPython import embed; embed()


    db.disconnect()