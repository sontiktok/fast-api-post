from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from schema.post_schema import PostRequest, PostResponse
from db.database import get_db
from controller import post_controller
from typing import List, Optional
from schema.user_schema import UserAuth
from validation.validation_file import validate_file, SUPPORTED_FILE_TYPES
from uuid import uuid4
from dotenv import load_dotenv
import os

load_dotenv()

AWS_BUCKET =os.getenv('AWS_BUCKET')
router = APIRouter(
    prefix='/post',
    tags=['post']
)

# @router.post('', response_model=PostResponse)
# def create(request: PostRequest, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     return post_controller.create(db,request,current_user)

@router.post('', response_model=PostResponse)
def create(request: PostRequest, db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    return post_controller.create(db,request,current_user)

# @router.get('', response_model=List[PostResponse])
# def posts(db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
#     return post_controller.get_all(db,current_user)


# @router.get('', response_model=List[PostResponse])
# def posts(db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
#     return post_controller.get_all(db,current_user)
# @router.get('', response_model=List[PostResponse])
# def posts(
#     skip: int = Query(default=0),
#     limit: int = Query(default=9),
#     db: Session = Depends(get_db),
#     current_user: UserAuth = Depends(get_current_user)
# ):
#     return post_controller.get_all(db, current_user, skip=skip, limit=limit)


@router.post('/update/{post_id}', response_model=PostResponse)
def update(post_id: int, request: PostRequest, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return post_controller.update(db, post_id, request)

# @router.post('/upload')
# async def upload(file: UploadFile):
#     if not file:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No file found')
#     contents, file_type = await validate_file(file)
#     file_name = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'
#     await s3_upload(contents=contents, key=file_name)
#     return {'file_name': file_name}

@router.get('/search-category/{category}', response_model=List[PostResponse])
def search_category(category: str,db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    return post_controller.search_category(category,db,current_user)

@router.get('/search-date/{date}', response_model=List[PostResponse])
def search_date(date: str,db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    return post_controller.search_date(date,db,current_user)

# @router.get('/search', response_model=List[PostResponse])
# def search_posts(category: Optional[str] = None, date: Optional[str] = None, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     if not category and not date:
#         return post_controller.get_all(db, current_user)
#     elif category and not date:
#         return post_controller.search_category(category, db, current_user)
#     elif date and not category:
#         return post_controller.search_date(date, db, current_user)
#     else:
#         return post_controller.search_by_category_and_date(category, date, db, current_user)
# @router.get('', response_model=List[PostResponse])
# def search_posts(category: Optional[str] = None, date: Optional[str] = None, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     if not category and not date:
#         return post_controller.get_all(db, current_user)
#     elif category and not date:
#         return post_controller.search_category(category, db, current_user)
#     elif date and not category:
#         return post_controller.search_date(date, db, current_user)
#     else:
#         return post_controller.search_by_category_and_date(category, date, db, current_user)
    
# @router.get('', response_model=List[PostResponse])
# def posts(
#     skip: int = Query(default=0),
#     limit: int = Query(default=9),
#     db: Session = Depends(get_db),
#     current_user: UserAuth = Depends(get_current_user)
# ):
#     return post_controller.get_all(db, current_user, skip=skip, limit=limit)

@router.get('', response_model=List[PostResponse])
def unified_posts_handler(
    category: Optional[str] = None,
    date: Optional[str] = None,
    skip: int = Query(default=0),
    limit: int = Query(default=9),
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
   return post_controller.get_all(db, current_user, category=category, date=date, skip=skip, limit=limit)