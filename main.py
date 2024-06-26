from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user,post,s3_service,like,comment
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
'''Create app'''
app = FastAPI()

'''Router'''
app.include_router(user.router)
app.include_router(post.router)
app.include_router(like.router)
app.include_router(comment.router)
app.include_router(s3_service.router)
app.include_router(authentication.router)

'''Define api'''
@app.get("/")
async def root():
    return {"message": "Hello World"}

origins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'http://localhost:3002'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)
'''Create db'''
models.Base.metadata.create_all(engine)

