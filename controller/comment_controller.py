from fastapi import HTTPException
from db.models import DbComment
from sqlalchemy.orm.session import Session
from schema.comment_schema import CommentRequest,CheckCommentRequest
from schema.user_schema import UserAuth
from datetime import datetime,timedelta
from services.ai_check_comment import predict_sentiment
from controller.user_controller import get_username_by_user_id
def get_all(postId: int,db: Session):
    comments = db.query(DbComment).filter(DbComment.post_id == postId).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this post")
    for comment in comments:
        comment.username = get_username_by_user_id(db, comment.user_id)
    return comments

def create(postId: int,request:CommentRequest,db: Session, current_user: UserAuth):
    new_comment = DbComment(
        content=request.content,
        status=request.status,
        created_at=datetime.now(),
        user_id=current_user.id,
        post_id=postId
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    new_comment.username = current_user.username
    return new_comment

def check_comment(request:CheckCommentRequest ):
    return predict_sentiment(request.comment)

