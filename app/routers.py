from datetime import timedelta
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from . import schemas, crud
from .auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_user
from .database import get_db
from .exceptions import UserDoesNotExistException, InvalidUsernameOrPasswordException, InvalidTokenException

router = APIRouter()


@router.get("/version")
def version():
    return {"version": "0.0.1"}


@router.post("/users/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_db = crud.create_user(db, user)
    return jsonable_encoder(user_db)


@router.post("/users/badges/")
def create_user_badge(user_badge: schemas.UserBadgeCreate, db: Session = Depends(get_db)):
    user_badge_db = crud.create_user_badge(db, user_badge)
    return jsonable_encoder(user_badge_db)


@router.get("/users/{user_id}/posts/", response_model=List[schemas.PostRead])
def get_posts_by_user_id(user_id: int, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = crud.get_posts_by_user_id(db, user_id, offset, limit)
    return jsonable_encoder(db_users)


@router.get("/users/", response_model=List[schemas.UserRead])
def get_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users_db = crud.get_users(db, offset, limit)
    return jsonable_encoder(users_db)


@router.post("/posts/")
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_db = crud.create_post(db, post)
    return jsonable_encoder(post_db)


@router.post("/posts/reaction")
def create_reaction(reaction: schemas.PostReactionBase, db: Session = Depends(get_db)):
    post_db = crud.increment_post_reaction(db, reaction)
    return jsonable_encoder(post_db)


@router.get("/posts/{post_id}/comments")
def get_comments(post_id: int, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts_db = crud.get_comments_by_post_id(db, post_id, offset, limit)
    return jsonable_encoder(posts_db)


@router.get("/posts/")
def get_posts(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts_db = crud.get_posts(db, offset, limit)
    return jsonable_encoder(posts_db)


@router.get("/post/search/")
def get_posts_by(close_to_me: bool = False, latitude: float = 0, longitude: float = 0, keyword: str = "",
                 offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_posts = crud.get_posts_by(db, close_to_me, keyword, latitude, longitude, offset, limit)
    return db_posts


@router.post("/login/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise InvalidUsernameOrPasswordException()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=schemas.UserRead)
async def read_users_me(
        current_user: Annotated[schemas.UserBase, Depends(get_current_active_user)]
        , db: Session = Depends(get_db)):
    token_data = current_user
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise InvalidTokenException()
    return user
