from sqlalchemy import DateTime, Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
	__tablename__ = 'posts'

	id = Column(BigInteger, primary_key=True)
	blog_name = Column(String)
	post_url = Column(String)
	reblogged_from_name = Column(String)
	reblogged_root_name = Column(String)
	type = Column(String)
	date = Column(DateTime)
