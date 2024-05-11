from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
import re
from schema.user_schema import User
class PostRequest(BaseModel):
    image_key: str
    caption: str
    category: str
    
class PostResponse(BaseModel):
    id: int
    image_key: str
    caption: str
    category: str
    created_at: datetime
    bookmark:bool
    # user: User
    # class Config():
    #     from_attributes  = True   