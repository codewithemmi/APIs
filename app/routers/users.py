
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models
from sqlalchemy.exc import IntegrityError
from app.schema import CreateResponse, CreateUser
from sqlalchemy.orm import Session
from .. utils import hashed, get_db
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from .. schema import Token, UserIndb, User
from .. utils import get_authenticate_user, get_current_active_user, timedelta, timezone, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, create_access_token
from . auth import get_the_current_user, verify_access_token,  oauth2_scheme
from jwt.exceptions import ExpiredSignatureError
from .. oau2th import create_token

router = APIRouter(tags=["Users"])


@router.post("/create-user", status_code=status.HTTP_201_CREATED, response_model=CreateResponse)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
     try:
          user.password = hashed(user.password)
          created_user = models.User(**user.dict())
          db.add(created_user)
          db.commit()
          db.refresh(created_user)
          return created_user
     except IntegrityError:
          raise HTTPException(status_code=status.HTTP_302_FOUND, detail="data already exist")
     
     
          
@router.get("/get-createuser/{id}", response_model=CreateResponse)
def get_user(id: int, db: Session = Depends(get_db), token_data: str = Depends(get_the_current_user)):
     user = db.query(models.User).filter(models.User.id == id).first()
     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} doesn't exist")
     return user

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) ->Token:
     database = db.query(models.User)
     user = get_authenticate_user(database, form_data.username, form_data.password, form_data)
     if not user:
               raise HTTPException(
                                   status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail="Incorrect username or password",
                                   headers={"WWW-Authenticate": "Bearer"},
                              )
     access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
     access_token = create_access_token(data={"sub": user.username}, expire_delta=access_token_expire)
     return Token(access_token=access_token, token_type="bearer")
   
     
@router.get("/users/me/",response_model=User)
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]):
     return current_user

          
@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/verify-token/")
def verify_token(token: str, credential_exception: str | None = None):
     try:
          token_data = verify_access_token(token, credential_exception)

     except ExpiredSignatureError:
          return {"exp": "token has expired"}
     return token_data



