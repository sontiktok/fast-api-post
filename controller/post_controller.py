from fastapi import HTTPException, status
from schema.post_schema import PostRequest
from sqlalchemy.orm.session import Session
from db.models import DbPost,DBLike
from schema.user_schema import UserAuth
import datetime
from fastapi import status
# from services.s3_services import create_presigned_url
from services.s3_server import server_create_presigned_url
from dotenv import load_dotenv
import os

load_dotenv()

AWS_BUCKET =os.getenv('AWS_BUCKET')
# def create(db: Session, request: PostRequest,current_user:UserAuth):
#   new_post = DbPost(
#     image_key = request.image_key,
#     caption = request.caption,
#     category = request.category,
#     created_at = datetime.datetime.now(),
#     user_id = current_user.id
#   )
#   db.add(new_post)
#   db.commit()
#   db.refresh(new_post)
#   return new_post

def create(db: Session, request: PostRequest,current_user:UserAuth):
  new_post = DbPost(
    image_key = request.image_key,
    caption = request.caption,
    category = request.category,
    created_at = datetime.datetime.now(),
    user_id = current_user.id
  )
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  new_post_with_bookmark = new_post.__dict__.copy()
  new_post_with_bookmark["bookmark"] = False
  return new_post_with_bookmark

# def get_all(db: Session,current_user:UserAuth):
#    posts = db.query(DbPost).filter().all()
#    return posts

# def get_all(db: Session,current_user:UserAuth):
#     posts = db.query(DbPost).filter().all()
#     for post in posts:
#       post.image_key = server_create_presigned_url(AWS_BUCKET,post.image_key)
#     return posts

def get_all(db: Session, current_user: UserAuth):
    posts = db.query(DbPost).all()
    liked_post_ids = {like.postId for like in db.query(DBLike).filter(DBLike.userId == current_user.id).all()}
    for post in posts:
        post.bookmark = post.id in liked_post_ids
        post.image_key = server_create_presigned_url(AWS_BUCKET,post.image_key)
    return posts

def update(db: Session, post_id: int, request: PostRequest, current_user: UserAuth):
    post = db.query(DbPost).filter(DbPost.id == post_id, DbPost.user_id == current_user.id).first()
    if post:
        if request.caption:
            post.caption = request.caption
        if request.image_key:
            post.image_key = request.image_key
        db.commit()
        db.refresh(post)
        return post
    else:
        return None
    
def search_category(category,db: Session, current_user: UserAuth):
    posts = db.query(DbPost).filter(DbPost.category == category).all()
    liked_post_ids = {like.postId for like in db.query(DBLike).filter(DBLike.userId == current_user.id).all()}
    for post in posts:
        post.bookmark = post.id in liked_post_ids
        post.image_key = server_create_presigned_url(AWS_BUCKET,post.image_key)
    return posts