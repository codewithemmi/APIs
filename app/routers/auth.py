from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..utils import get_db, verify_password
from app.schema import UserLogin, Token, TokenData
from .. import models
from .. oau2th import create_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..utils import SECRET_KEY, ALGORITHM
import jwt
from jwt.exceptions import ExpiredSignatureError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login (userlogin: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == userlogin.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ivalid credentials")
    if not verify_password(userlogin.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ivalid credentials")
    access_token = create_token(data={"sub": user.username})
    return {"access_token": access_token, "Bearer": "bearer"}


def verify_access_token(token: str, credential_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except ValueError as error:
        raise credential_exception
    return token_data


def get_the_current_user(token: str = Depends(oauth2_scheme)):
        credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="INVALID CREDENTIALS", headers={"WWW-Authenticate": "Beareer"})
        return verify_access_token(token, credential_exception)
        
            

