from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from app.schema import UserIndb, User, TokenData, Token
from . import models

from passlib.context import CryptContext
from app.database import SessionLocal
from . main import Session



SECRET_KEY = "5b9892607beb3c28ba594c809f474109f02fc8d913356d5aabcd583785e60fa0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
     return pwd_context.verify(password, hashed_password)



def get_db():
     db = SessionLocal()
     try:
          yield db
     finally:
          db.close()



def get_user(db, username: str):
                user = db.filter(models.User.username == username).first()
                if user:
                   return UserIndb(**user.__dict__)
                        #id=user.id, username=user.username, password=user.password, email=user.email, disabled=user.disabled, created_at=user.created_at)     
                #UserIndb(id=db.id, username=db.username, password=db.password, email=db.email, disabled=db.disabled, created_at=db.created_at)  
     

     
def get_authenticate_user(database, username: str, password: str):
     user = get_user(database, username)
     if user is None:
          return False
     if not verify_password(password, user.password):
          return False
     return user


def create_access_token(data: dict, expire_delta: timedelta):
     to_encode = data.copy()
     expire = datetime.utcnow().replace(tzinfo=timezone.utc) + expire_delta
     to_encode.update({"exp": expire})
     jwt_encode = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
     return jwt_encode



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
             raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    database = db.query(models.User)
    user = get_user(database, username=token_data.username)
    if user is None:
           raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
     if current_user.disabled:
          raise HTTPException(status_code=400, detail="Inactive user")
     return current_user



def userdb(token_data, db: Session = Depends(get_db)):
     user = db.query(models.User).filter(models.User.username == token_data).first()
     return user.id

