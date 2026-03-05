from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from entries import router as entries_router
from user import router as users_router
from auth_utils import get_current_user
from database import engine, Base
import models

# Automatically create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import APIRouter

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(entries_router)
api_router.include_router(users_router)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "theme": current_user.theme
    }
