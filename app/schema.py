from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class PostBase(BaseModel):
     title: str
     content: str
     published: bool


class PostCreate(PostBase):
     pass
     

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    


class PostResponse(PostBase):
     id: int
     created_at: datetime
     owner_id: int
     owner: UserOut
     
class Post(BaseModel):
     id: int
     title: str
     content: str
     published: bool
     created_at: datetime
     owner_id: int
     
     

class PostOut(BaseModel):
     Post: PostResponse
     votes: int



# create user Pydantic/Model
class CreateUser(BaseModel):
     username: str
     email: EmailStr
     password: str
     disabled: bool

# create user response model, using Pydantic.
class CreateResponse(BaseModel):
     id: int
     username: str
     email: EmailStr
     created_at: datetime


# creating access token models, using Pydantic.

class Token(BaseModel):
     access_token: str
     token_type: str

class TokenData(BaseModel):
     username: str | None = None


class User(BaseModel):
    id: int
    username: str
    email: str | None = None
    disabled: bool | None = None
    created_at: datetime


class UserIndb(User):
     password: str
     
#toturial

class UserLogin(BaseModel):
     email: EmailStr
     password: str


class Tokendata(BaseModel):
     access_token: str 
     token_type: str

class Vote(BaseModel):
     post_id: int
     vote_dir: int = conint(le=1)



     
     