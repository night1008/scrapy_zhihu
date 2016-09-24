#coding: utf-8
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://root:100815@127.0.0.1:3306/zhihu')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Collection(Base):
	__tablename__ = 'collection'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String, default='')	
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime)

	def __repr__(self):
		return "<Collection(name='%s')>" % (self.name)

if __name__ == '__main__':
	print 'test sqlachemy'
	print Collection.__table__
	collection = Collection(id="1", name='test')
	print collection
	session = Session()
	session.add(collection)
	session.commit()