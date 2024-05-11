from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

# Define table
class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)  
    # email = Column(String(255), index=True)     
    password = Column(String(255))
    created_at = Column(DateTime)             
    items = relationship('DbPost', back_populates='user')
    
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
    
class DBLike(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer, ForeignKey('post.id'))
    userId = Column(Integer)
    post = relationship('DbPost', back_populates='like')
    