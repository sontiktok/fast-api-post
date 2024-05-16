from pydantic import BaseModel, EmailStr, validator
import re

class User(BaseModel):
    username: str
    class Config():
        from_orm  = True 
        
class UserAuth(BaseModel):
  id: int
  username: str
  email: str
        
class UserRequest(BaseModel):
    username: str
    # email: EmailStr
    password: str | None

    @validator('username')
    def username_length(cls, v):
        if len(v) < 3 or len(v) > 16:
            raise ValueError('Username must be between 3 and 16 characters')
        return v

    @validator('password')
    def password_complexity(cls, v):
        if len(v) < 8 or len(v) > 32:
            raise ValueError('Password must be between 8 and 32 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserResponse(BaseModel):
    username: str
    # email: str
    class Config():
        from_attributes = True