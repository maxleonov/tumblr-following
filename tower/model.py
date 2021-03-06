from sqlalchemy import DateTime, Column, BigInteger, String, Integer, UniqueConstraint
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


class Following(Base):
    __tablename__ = 'following'
    __table_args__ = (UniqueConstraint('user_name', 'blog_name'),)

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    blog_name = Column(String)
    title = Column(String)
    description = Column(String)
    url = Column(String)
