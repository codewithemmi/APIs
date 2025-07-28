from fastapi import FastAPI
from app import models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.schema import PostCreate, PostResponse, CreateResponse, CreateUser
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse
from app.routers import users, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware



models.Base.metadata.create_all(bind=engine)




app = FastAPI()



origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
def root():
   return {"Welcome to my APi"}




