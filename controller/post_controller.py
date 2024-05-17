from schema.post_schema import PostRequest
from sqlalchemy.orm.session import Session
from db.models import DbPost,DBLike
from schema.user_schema import UserAuth
import datetime
from services.s3_server import server_create_presigned_url
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta
from typing import List, Optional

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
    created_at = datetime.now(),
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

# def get_all(db: Session, current_user: UserAuth):
#     posts = db.query(DbPost).all()
#     liked_post_ids = {like.postId for like in db.query(DBLike).filter(DBLike.userId == current_user.id).all()}
#     for post in posts:
#         post.bookmark = post.id in liked_post_ids
#         post.image_key = server_create_presigned_url(AWS_BUCKET,post.image_key)
#     return posts


# def get_all(db: Session, current_user: UserAuth, skip: int = 0, limit: int = 9):
#     posts = db.query(DbPost).offset(skip).limit(limit).all()
#     liked_post_ids = {like.postId for like in db.query(DBLike).filter(DBLike.userId == current_user.id).all()}
#     for post in posts:
#         post.bookmark = post.id in liked_post_ids
#         post.image_key = server_create_presigned_url(AWS_BUCKET, post.image_key)
#     return posts

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

def search_date(date: str, db: Session, current_user: UserAuth):
    # Chuyển đổi ngày nhập vào từ chuỗi theo định dạng 'DD-MM-YYYY' thành datetime
    search_date = datetime.strptime(date, '%d-%m-%Y')
    next_day = search_date + timedelta(days=1)
    print(f"Searching posts created on or before: {search_date}")

    # Truy vấn tất cả bài đăng được tạo vào ngày nhập vào hoặc trước đó
    posts = db.query(DbPost).filter(DbPost.created_at < next_day).all()
    print(f"Number of posts retrieved: {len(posts)}")

    # Lấy danh sách các ID bài đăng mà người dùng hiện tại đã thích
    liked_post_ids = {like.postId for like in db.query(DBLike).filter(DBLike.userId == current_user.id).all()}
    print(f"Number of liked posts: {len(liked_post_ids)}")

    # Đánh dấu bài đăng đã được thích và tạo URL ký tên trước cho hình ảnh
    for post in posts:
        post.bookmark = post.id in liked_post_ids
        post.image_key = server_create_presigned_url(AWS_BUCKET, post.image_key)

    return posts

def search_by_category_and_date(category: str, date: str, db: Session, current_user: UserAuth):
    # Chuyển đổi ngày nhập vào từ chuỗi theo định dạng 'DD-MM-YYYY' thành datetime
    search_date = datetime.strptime(date, '%d-%m-%Y')
    next_day = search_date + timedelta(days=1)
    print(f"Searching posts in category '{category}' created on or before: {search_date}")

    # Truy vấn tất cả bài đăng được tạo vào ngày nhập vào hoặc trước đó và thuộc danh mục chỉ định
    posts = db.query(DbPost).filter(DbPost.category == category, DbPost.created_at < next_day).all()
    print(f"Number of posts retrieved: {len(posts)}")

    # Lấy danh sách các ID bài đăng mà người dùng hiện tại đã thích
    liked_post_ids = {like.postId for like in db.query(DBLike).filter(DBLike.userId == current_user.id).all()}
    print(f"Number of liked posts: {len(liked_post_ids)}")

    # Đánh dấu bài đăng đã được thích và tạo URL ký tên trước cho hình ảnh
    for post in posts:
        post.bookmark = post.id in liked_post_ids
        post.image_key = server_create_presigned_url(AWS_BUCKET, post.image_key)

    return posts


def get_all(db: Session, current_user: UserAuth, category: Optional[str] = None, date: Optional[str] = None, skip: int = 0, limit: int = 9):
    query = db.query(DbPost)

    if category:
        query = query.filter(DbPost.category == category)

    if date:
        search_date = datetime.strptime(date, '%d-%m-%Y')
        next_day = search_date + timedelta(days=1)
        query = query.filter(DbPost.created_at < next_day)

    posts = query.offset(skip).limit(limit).all()
    liked_post_ids = {like.postId for like in db.query(DBLike).filter(DBLike.userId == current_user.id).all()}

    for post in posts:
        post.bookmark = post.id in liked_post_ids
        post.image_key = server_create_presigned_url(AWS_BUCKET, post.image_key)

    return posts

