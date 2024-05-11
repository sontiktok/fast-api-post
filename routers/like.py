from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from controller import like_controller
from schema.user_schema import UserAuth
from auth.oauth2 import get_current_user


#define router
router = APIRouter(
    prefix='/like',
    tags=['like']
)

@router.get('/{postId}',)
def like_post(postId:int, db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    return like_controller.like_post(postId,db, current_user)

@router.delete('/cancle/{postId}',)
def cancle(postId:int, db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    return like_controller.cancle(postId,db, current_user)