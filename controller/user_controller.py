from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from db.models import DbUser
from schema.user_schema import UserResponse
from db.hashing import Hash
from sqlalchemy.orm.session import Session
from fastapi import status
import datetime

def create_user(db: Session, request: UserResponse):
    try:
        # Kiểm tra tồn tại người dùng
        existing_user = db.query(DbUser).filter(DbUser.username == request.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Kiểm tra tồn tại email
        # existing_email = db.query(DbUser).filter(DbUser.email == request.email).first()
        # if existing_email:
        #     raise HTTPException(status_code=400, detail="Email already exists")

        # Tạo người dùng mới
        new_user = DbUser(
            username=request.username,
            # email=request.email,
            password=Hash.bcrypt(request.password),
            created_at=datetime.datetime.now()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except SQLAlchemyError as e:
        # Xử lý lỗi liên quan đến cơ sở dữ liệu
        db.rollback()  # Rollback thay đổi nếu có lỗi
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

    except Exception as e:
        # Xử lý các lỗi khác không mong đợi
        db.rollback()  # Rollback thay đổi nếu có lỗi
        raise HTTPException(status_code=500, detail=str(e))
    
    
def get_user_by_username(db: Session, username: str):
  user = db.query(DbUser).filter(DbUser.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return user

def get_username_by_user_id(db: Session, user_id: int):
    # Truy vấn lấy thông tin người dùng dựa trên user_id
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        # Nếu không tìm thấy người dùng, ném ra HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with user_id {user_id} not found")
    # Trả về username của người dùng
    return user.username
    
