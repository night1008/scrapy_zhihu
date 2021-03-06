# coding: utf-8
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://root:100815@127.0.0.1:3306/zhihu?charset=utf8')
Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()

class Collection(Base):
    __tablename__ = 'collection'
    UPDATED_DAY = 10

    id = Column(Integer, primary_key=True)        # 收藏夹ID，与知乎对应
    title = Column(String)                        # 名称
    user_token = Column(String, default=None)    # 收藏者域名标识
    description = Column(String, default=None)    # 描述
    review_count = Column(String, default=0)    # 评论数
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)  #可用于更新机制

    def is_need_update(self):
        return self.updated_at + timedelta(days=self.UPDATED_DAY) > datetime.now()  

    def __repr__(self):
        return "<Collection(name='%s')>" % (self.title)


class Answer(Base):
    __tablename__ = 'answer'
    UPDATED_DAY = 5

    id = Column(Integer, primary_key=True)        # 答案ID，与知乎对应
    user_token = Column(String, default=None)        # 回答者域名标识
    question_id = Column(Integer)                    # 问题ID
    summary = Column(Text)                            # 摘要
    content = Column(Text)                            # 回答内容
    vote_up = Column(Integer)                        # 点赞数
    vote_down = Column(Integer)                        # 反对数
    review_count = Column(Integer, default=None)    # 评论数
    published_at = Column(DateTime, default=None)    # 发布时间
    edited_at = Column(DateTime, default=None)        # 编辑时间
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def is_need_update(self):
        return self.updated_at + timedelta(days=self.UPDATED_DAY) > datetime.now()

    def __repr__(self):
        return "<Answer(content='%s')>" % (self.content[:20])


class Question(Base):
    __tablename__ = 'question'
    UPDATED_DAY = 10

    id = Column(Integer, primary_key=True)    # 问题ID，与知乎对应
    user_token = Column(String, default=None)    # 提问者域名标识
    title = Column(String)                        # 标题
    content = Column(Text)                        # 内容
    following_count = Column(Integer)           # 关注数
    review_count = Column(Integer)                # 评论数
    answer_count = Column(Integer)                # 回答数
    visit_count = Column(Integer)                # 访问数
    is_top = Column(Boolean, default=None)        # 是否是精华问题
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def is_need_update(self):
        return self.updated_at + timedelta(days=self.UPDATED_DAY) > datetime.now()

    def __repr__(self):
        return "<Question(title='%s')>" % (self.title)


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    kwargs = Column(Integer)
    state = Column(String)
    error_info = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return "<Task(name='%s')>" % (self.name)


class Author(Base):
    __tablename__ = 'author'
    UPDATED_DAY = 10

    id = Column(Integer, primary_key=True)
    token = Column(String)                # 个性域名标志
    name = Column(String)                # 名称
    biography = Column(String)            # 个人简介
    pic_url = Column(String)            # 头像链接
    description = Column(Text)            # 个人描述
    location = Column(String)            # 所在地
    business = Column(String)            #
    gender = Column(Integer)            # 性别
    employment = Column(String)
    education = Column(String)            # 教育经历
    follower_count = Column(Integer)    # 被关注数
    followee_count = Column(Integer)    # 关注数
    thank_count = Column(Integer)        # 用户感谢数
    aggre_count = Column(Integer)        # 用户赞同数
    question_count = Column(Integer)    # 问题数
    answer_count = Column(Integer)        # 回答数
    post_count = Column(Integer)        # 文章数
    collection_count = Column(Integer)  # 收藏夹数
    log_count = Column(Integer)            # 公共编辑数
    visit_count = Column(Integer)        # 用户访问数
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def is_need_update(self):
        return self.updated_at + timedelta(days=self.UPDATED_DAY) > datetime.now()

    def __repr__(self):
        return "<Author(name='%s')>" % (self.name)


class CollectionAnswer(Base):
    __tablename__ = 'collection_answer'

    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer)
    answer_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return "<CollectionAnswer(collection_id='%s', answer_id='%s')>" % \
               (self.collection_id, self.answer_id)

# memo: 未登录下得不到
class AuthorFollower(Base):
    __tablename__ = 'user_follower'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    follower_id = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class AuthorFollowee(Base):
    __tablename__ = 'user_followee'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    followee_id = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	email = Column(String)
	password = Column(String)
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)

    # def is_authenticated(self):
    #     return True

    # def is_active(self):
    #     return True

    # def is_anonymous(self):
    #     return False

    # def get_id(self):
    #     return self.id

    # def get_user(self, session):
    #     pass