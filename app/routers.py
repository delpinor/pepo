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
def add_badge_to_user(user_badge: schemas.UserBadgeCreate, db: session = Depends(get_db)):
    user_badge_db = crud.create_user_badge(db, user_badge)
    return jsonable_encoder(user_badge_db)


@router.get("/users/{user_id}/posts/", response_model=List[schemas.PostRead])
def get_posts_by_user_id(user_id: int, offset: int = 0, limit: int = 100, db: session = Depends(get_db)):
    db_users = crud.get_posts_by_user_id(db, user_id, offset, limit)
    return jsonable_encoder(db_users)


@router.get("/users/", response_model=List[schemas.UserRead])
def get_users(offset: int = 0, limit: int = 100, db: session = Depends(get_db)):
    users_db = crud.get_users(db, offset, limit)
    return jsonable_encoder(users_db)


@router.post("/posts/")
def create_post(post: schemas.PostCreate, db: session = Depends(get_db)):
    post_db = crud.create_post(db, post)
    return jsonable_encoder(post_db)


@router.post("/posts/reaction")
def create_reaction(reaction: schemas.PostReactionBase, db: session = Depends(get_db)):
    post_db = crud.increment_post_reaction(db, reaction)
    return jsonable_encoder(post_db)


@router.get("/posts/{post_id}/comments")
def get_comments(post_id: int, offset: int = 0, limit: int = 100, db: session = Depends(get_db)):
    posts_db = crud.get_comments_by_post_id(db, post_id, offset, limit)
    return jsonable_encoder(posts_db)


@router.get("/posts/")
def get_posts(offset: int = 0, limit: int = 100, db: session = Depends(get_db)):
    posts_db = crud.get_posts(db, offset, limit)
    return jsonable_encoder(posts_db)
