from sqlalchemy.orm import Session, joinedload
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, offset: int = 0, limit: int = 100):
    db_users = db.query(models.User).options(joinedload(models.User.badges))
    return db_users.offset(offset).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    user_query = db.query(models.User)
    user_query.filter(models.User.user_id == user_id)
    return user_query.first()


def create_user_badge(db: Session, user_badge: schemas.UserBadgeCreate):
    q = models.users_badges.insert().values(user_id=user_badge.user_id, badge_id=user_badge.badge_id)
    db.execute(q)
    db.commit()


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, offset: int = 0, limit: int = 100):
    posts = db.query(models.Post)
    return posts.offset(offset).limit(limit).all()
