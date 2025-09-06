from . import model,calculations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from .routers import post,user,votes,auth
from .config import settings



# model.Base.metadata.create_all(bind=engine)
 
app=FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(votes.router)
app.include_router(auth.router)
# app.include_router(calculations.router)
