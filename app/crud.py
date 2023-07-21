from fastapi import Query
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

CLOSE_TO_ME_MEANS_KM = 2


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate):
    user.password = get_password_hash(user.password)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, offset: int = 0, limit: int = 100):
    query = db.query(models.User).offset(offset).limit(limit).all()
    users = []
    for user in query:
        user_json = jsonable_encoder(user)
        json_badges = []
        for user_badge_association in user.badges:
            json_badges.append(jsonable_encoder(user_badge_association.badge))
        user_json["badges"] = json_badges
        users.append(user_json)
    return users


def get_user(db: Session, username: str = None):
    db_user = db.query(models.User).filter(models.User.username == username).one()
    return db_user


def get_user_by_id(db: Session, user_id: int):
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    return user_query.first()


def create_user_badge(db: Session, user_badge: schemas.UserBadgeCreate):
    db_user_badge = models.UserBadge(**user_badge.dict())
    db.add(db_user_badge)
    db.commit()
    db.refresh(db_user_badge)
    return db_user_badge


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    initialize_reaction_counter(db, db_post.post_id)
    return db_post


def initialize_reaction_counter(db: Session, post_id: int):
    db_reactions = db.query(models.Reaction).all()
    for reaction in db_reactions:
        db_reaction_post = models.PostReaction(post_id=post_id, reaction_id=reaction.reaction_id)
        db.add(db_reaction_post)
    db.commit()


def get_posts_by_user_id(db: Session, user_id: int, offset: int = 0, limit: int = 100):
    db_posts = db.query(models.Post).filter(models.Post.user_id == user_id)
    return db_posts.offset(offset).limit(limit).all()


def get_comments_by_post_id(db: Session, post_id: int, offset: int = 0, limit: int = 100):
    db_posts = db.query(models.Post).filter(models.Post.in_reply_to_post_id == post_id). \
        offset(offset).limit(limit).all()
    return db_posts


def get_posts(db: Session, offset: int = 0, limit: int = 100):
    db_posts = db.query(models.Post).offset(offset).limit(limit)
    return posts_with_reaction_count(db_posts)


def posts_with_reaction_count(db_posts: Query):
    json_posts = []
    for post in db_posts:
        json_post = jsonable_encoder(post)
        json_reactions = []
        for post_reaction_association in post.reactions:
            reaction = jsonable_encoder(post_reaction_association.reaction)
            reaction["reaction_count"] = jsonable_encoder(post_reaction_association)["reaction_count"]
            json_reactions.append(reaction)
        json_post["reactions"] = json_reactions
        json_posts.append(json_post)
    return json_posts


def get_posts_by_creation_date(db: Session, offset: int = 0, limit: int = 100):
    db_posts = db.query(models.Post). \
        order_by(models.Post.created_at.desc()) \
        .offset(offset).limit(limit).all()
    return posts_with_reaction_count(db_posts)


def get_post_by_area(db: Session, keyword: str = "", latitude: float = 0, longitude: float = 0, offset: int = 0,
                     limit: int = 100):
    db_posts = db.query(models.Post).filter(
        (func.degrees(
            func.acos(
                func.sin(func.radians(latitude)) * func.sin(func.radians(models.Post.latitude)) +
                func.cos(func.radians(latitude)) * func.cos(func.radians(models.Post.latitude)) *
                func.cos(func.radians(longitude - models.Post.longitude))
            )
        ) * 60 * 1.1515 * 1.609344) <= CLOSE_TO_ME_MEANS_KM, models.Post.text.ilike(f"%{keyword}%"),
        models.Post.in_reply_to_post_id == 0).order_by(models.Post.created_at.desc()).offset(offset).limit(limit).all()
    return db_posts


def increment_post_reaction(db: Session, reaction: schemas.PostReactionBase):
    try:
        db_reaction = models.PostReaction(**reaction.dict())
        db.add(db_reaction)
        db.commit()
        db.refresh(db_reaction)
        return db_reaction
    except IntegrityError:
        db.rollback()
        db_reaction = db.query(models.PostReaction). \
            filter(models.PostReaction.post_id == reaction.post_id,
                   models.PostReaction.reaction_id == reaction.reaction_id).first()
        db_reaction.reaction_count += 1
        db.commit()


def get_posts_by(db: Session, close_to_me: bool, keyword: str, latitude: float, longitude: float,
                 offset: int, limit: int):
    if close_to_me:
        db_posts = get_post_by_area(db, keyword, latitude, longitude, offset, limit)
    else:
        db_posts = db.query(models.Post).filter(models.Post.text.ilike(f"%{keyword}%"),
                                                models.Post.in_reply_to_post_id == 0).\
            order_by(models.Post.created_at.desc()).offset(offset).limit(limit).all()
    return posts_with_reaction_count(db_posts)
