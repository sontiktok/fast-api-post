from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from controller import comment_controller
from schema.user_schema import UserAuth
from auth.oauth2 import get_current_user
from schema.comment_schema import CommentRequest,CommentResponse,CheckCommentRequest
from typing import List, Optional


#define router
router = APIRouter(
    prefix='/comment',
    tags=['comment']
)

@router.get('/{postId}',response_model=List[CommentResponse])
def get_list_comment(postId:int,db: Session = Depends(get_db)):
    return comment_controller.get_all(postId,db)  

@router.post('/create/{postId}',response_model=CommentResponse)
def create_comment(postId:int ,request: CommentRequest, db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    return comment_controller.create(postId,request,db, current_user)

@router.post('/check_comment')
def check_comment(request: CheckCommentRequest):
    return comment_controller.check_comment(request)