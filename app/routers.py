from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session

from . import schemas, crud
from .database import get_db
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/version")
def version():
    return {"version": "0.0.1"}


@router.post("/users/")
def create_user(user: schemas.UserCreate, db: session = Depends(get_db)):
    user_db = crud.create_user(db, user)
    return jsonable_encoder(user_db)


@router.post("/users/badges/")
def create_user(user_badge: schemas.UserBadgeCreate, db: session = Depends(get_db)):
    user_badge_db = crud.create_user_badge(db, user_badge)
    return jsonable_encoder(user_badge_db)


@router.get("/users/", response_model=List[schemas.UserRead])
def get_users(offset: int = 0, limit: int = 100, db: session = Depends(get_db)):
    users_db = crud.get_users(db, offset, limit)
    return jsonable_encoder(users_db)


@router.post("/posts/")
def create_post(post: schemas.PostCreate, db: session = Depends(get_db)):
    post_db = crud.create_post(db, post)
    return jsonable_encoder(post_db)


@router.get("/posts/", response_model=List[schemas.PostRead])
def get_posts(offset: int = 0, limit: int = 100, db: session = Depends(get_db)):
    posts_db = crud.get_posts(db, offset, limit)
    return jsonable_encoder(posts_db)
