from . import model  # make sure this line loads all models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from .routers import post, user, votes, auth
from .config import settings

# ✅ Create tables after all models are imported
# model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origin = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(votes.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Hello CI/CD is successfully deployed"}
