import enum

from sqlalchemy import Column, Integer, String, Text,\
    DateTime, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship

from database import Base


feed_liker = Table(
    'feed_liker',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('feed_id', Integer, ForeignKey('feed.id'), primary_key=True)
)

comment_liker = Table(
    'comment_liker',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('comment_id', Integer, ForeignKey('comment.id'), primary_key=True)
)


class Feed(Base):
    __tablename__ = "feed"

    id = Column(Integer, primary_key=True)
    img = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    weather = Column(String, nullable=False)
    temperature = Column(String, nullable=False)
    sensitivity = Column(String, nullable=False)
    city = Column(String, nullable=False)
    district = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="feed_users")
    liker = relationship("User", secondary=feed_liker, backref="feed_likers")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="user_comments")
    liker = relationship("User", secondary=comment_liker,
                         backref="comment_likers")


class ProductLink(Base):
    __tablename__ = "product_link"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    feed_id = Column(Integer, ForeignKey("feed.id"), nullable=False)
    feed = relationship("Feed", backref="feed_product_links")
