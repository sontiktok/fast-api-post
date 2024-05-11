# from passlib.context import CryptContext

# pwd_cxt = CryptContext(schemes=['bcrypt'],deprecated="auto")

# class Hash():
#     def bcrypt(password: str):
#         return pwd_cxt.hash(password)
#     def verify(hashed_password,plain_password):
#         return pwd_cxt.verify(plain_password,hashed_password)

import bcrypt

class Hash():
    @staticmethod
    def bcrypt(password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')
    
    @staticmethod
    def verify(hashed_password, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))