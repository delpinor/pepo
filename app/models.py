import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


users_badges = Table(
    "users_badges",
    Base.metadata,
    Column("user_id", ForeignKey("users.user_id"), primary_key=True),
    Column("badge_id", ForeignKey("badges.badge_id"), primary_key=True)
)

posts_reactions = Table(
    "posts_reactions",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.post_id"), primary_key=True),
    Column("reaction_id", Integer, ForeignKey("reactions.reaction_id"), primary_key=True),
    Column("reaction_count", Integer)
)


class Badge(Base):
    __tablename__ = "badges"
    badge_id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(String)


class Reaction(Base):
    __tablename__ = "reactions"
    reaction_id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(String)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    device_token = Column(String, nullable=True)
    status = Column(String, default="active")

    badges = relationship("Badge", secondary=users_badges)
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(String)
    in_reply_to_post_id = Column(Integer, nullable=True)
    latitude = Column(Float(precision=32))
    longitude = Column(Float(precision=32))
    status = Column(String, default="active")
    user_id = Column(Integer, ForeignKey(column="users.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="posts")
    reactions = relationship("Reaction", secondary=posts_reactions)

