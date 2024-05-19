from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    password = Column(String(255))
    created_at = Column(DateTime)
    items = relationship('DbPost', back_populates='user')
    comments = relationship('DbComment', back_populates='user')

class DbPost(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    image_key = Column(String(255))
    caption = Column(String(255))
    category = Column(String(255))
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('DbUser', back_populates='items')
    like = relationship('DBLike', back_populates='post')
    comments= relationship('DbComment', back_populates='post')

class DBLike(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer, ForeignKey('post.id'))
    userId = Column(Integer)
    post = relationship('DbPost', back_populates='like')
    
    
class DbComment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))
    status =  Column(String(255))
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('DbPost', back_populates='comments')
    user = relationship('DbUser', back_populates='comments')