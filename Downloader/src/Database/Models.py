from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# import pymssql
# from Facebook.Database import get_session
from .__init__ import get_engine

Base = declarative_base()


class Page(Base):
	__tablename__ = 'FB_Page'

	id = Column(String(100), primary_key = True, autoincrement = False)

	name = Column(String(250), nullable = False)
	about = Column(String(5000))
	likes = Column(BigInteger)
	link = Column(String(500))


class Post(Base):
	__tablename__ = 'FB_Post'

	id = Column(String(100), primary_key = True, autoincrement = False)
	page_id = Column(String(100))

	message = Column(String(7000))
	link = Column(String(500))
	created_time = Column(String(250))
	type = Column(String(250))
	name = Column(String(250))
	likes = Column(BigInteger)

class Comment(Base):
	__tablename__ = 'FB_Comment'

	id = Column(String(100), primary_key = True, autoincrement = False)
	post_id = Column(String(100))
	user_id = Column(String(100))
	parent = Column(String(100))

	message = Column(String(5000))

	like_count = Column(BigInteger)
	comment_count = Column(BigInteger)

	created_time = Column(String(100))


class User(Base):
	__tablename__ = 'FB_User'

	id = Column(String(100), primary_key = True, autoincrement = False)

	first_name = Column(String(200))
	middle_name = Column(String(200))
	last_name = Column(String(200))
	name = Column(String(600))

	min_age_range = Column(BigInteger)
	max_age_range = Column(BigInteger)
	gender = Column(String(50))
	political = Column(String(100))
	relationship_status = Column(String(50))
	religion = Column(String(50))
	location = Column(String(50))
	about = Column(String(1000))

engine = get_engine()
Base.metadata.create_all(engine)