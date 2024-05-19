from pydantic import BaseModel
from datetime import datetime
import re
from schema.user_schema import User
class CommentRequest(BaseModel):
    content: str
    status: str
class CommentResponse(BaseModel):
    id: int
    content: str
    status: str
    created_at: datetime
    username: str
    user_id: int
    post_id: int  
    
class CheckCommentRequest(BaseModel):
    comment: str