import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Table
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import relationship
from .database import Base
import geopy.distance
from sqlalchemy import func


class UserBadge(Base):
    __tablename__ = "users_badges"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    badge_id = Column(Integer, ForeignKey("badges.badge_id"), primary_key=True)

    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="users")

    def __str__(self):
        return self.badge.description


class PostReaction(Base):
    __tablename__ = "posts_reactions"
    post_id = Column(Integer, ForeignKey("posts.post_id"), primary_key=True)
    reaction_id = Column(Integer, ForeignKey("reactions.reaction_id"), primary_key=True)
    reaction_count = Column(Integer, default=0)

    post = relationship("Post", back_populates="reactions")
    reaction = relationship("Reaction", back_populates="posts")


class Badge(Base):
    __tablename__ = "badges"
    badge_id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(String, unique=True)

    users = relationship("UserBadge", back_populates="badge")


class Reaction(Base):
    __tablename__ = "reactions"
    reaction_id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(String, unique=True)

    posts = relationship("PostReaction", back_populates="reaction")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    device_token = Column(String, nullable=True)
    status = Column(String, default="active")

    badges = relationship("UserBadge", back_populates="user")
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(String)
    in_reply_to_post_id = Column(Integer, nullable=True, default=0)
    latitude = Column(Float(precision=32))
    longitude = Column(Float(precision=32))
    status = Column(String, default="active")
    user_id = Column(Integer, ForeignKey(column="users.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="posts")
    reactions = relationship("PostReaction", back_populates="post")

    @hybrid_method
    def distance_from(self, coords) -> float:
        coords_post = (self.latitude, self.longitude)
        return geopy.distance.geodesic(coords_post, coords).km

    @distance_from.expression
    def distance_from(cls, coords) -> float:
        coords_post = (cls.latitude, cls.longitude)
        return geopy.distance.geodesic(coords_post, coords).km



