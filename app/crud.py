from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.serializer import dumps
from sqlalchemy.orm import Session, joinedload, join, subqueryload, contains_eager, Query
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
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
    return db_post


def get_posts_by_user_id(db: Session, user_id: int, offset: int = 0, limit: int = 100):
    db_posts = db.query(models.Post).filter(models.Post.user_id == user_id)
    return db_posts.offset(offset).limit(limit).all()


def get_comments_by_post_id(db: Session, post_id: int, offset: int = 0, limit: int = 100):
    db_posts = db.query(models.Post).filter(models.Post.in_reply_to_post_id == post_id).\
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


def get_post_by_area(db: Session, post_area: schemas.PostByAreaRead, offset: int = 0, limit: int = 100):
    db_posts = db.query(models.Post).filter(
        models.Post.distance_from((post_area.latitude, post_area.longitude)) <= post_area.distance_in_km)
    return db_posts.offset(offset).limit(limit).all()


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
