from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from schema.user_schema import UserRequest, UserResponse
from controller import user_controller
#define router
router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('',response_model=UserResponse)
def create_user(request: UserRequest,db: Session = Depends(get_db)):
    return user_controller.create_user(db,request)