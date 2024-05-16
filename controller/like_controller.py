from fastapi import HTTPException
from db.models import DBLike
from sqlalchemy.orm.session import Session
from schema.user_schema import UserAuth



def like_post(postId: int, db: Session, current_user: UserAuth):
    # Kiểm tra xem đã tồn tại mục với userId và postId cụ thể hay chưa
    existing_like = db.query(DBLike).filter(DBLike.postId == postId, DBLike.userId == current_user.id).first()
    
    # Nếu đã tồn tại, ném một ngoại lệ HTTPException
    if existing_like:
        raise HTTPException(status_code=400, detail="User already liked this post")
    
    # Nếu chưa tồn tại, tạo một mục mới
    like = DBLike(postId=postId, userId=current_user.id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def cancle(postId: int, db: Session, current_user: UserAuth):
    like_to_cancel = db.query(DBLike).filter(DBLike.postId == postId, DBLike.userId == current_user.id).first()
    
    if not like_to_cancel:
        raise HTTPException(status_code=404, detail="Like not found")
    
    db.delete(like_to_cancel)
    db.commit()
    return "Unlike post"

