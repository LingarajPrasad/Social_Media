from fastapi import FastAPI
from . import models
from .database import engine
from passlib.context import CryptContext
from .routers import post,user,auth,vote
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = 'auto')
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# models.Base.metadata.create_all(bind = engine)
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
#entry point
@app.get("/")
async def root():
    return {"message": "welcome to my API"}