from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# Badges
class BadgeBase(BaseModel):
    badge_id: int
    description: str

    class Config:
        orm_mode = True


# UserBadges
class UserBadgeBase(BaseModel):
    user_id: int
    badge_id: int

    class Config:
        orm_mode = True


class UserBadgeCreate(UserBadgeBase):
    pass


class UserBadgeRead(UserBadgeBase):
    badge: list[UserBadgeBase] = []

    class Config:
        orm_mode = True


# Reactions
class ReactionBase(BaseModel):
    reaction_id: int
    description: str
    reaction_count: int

    class Config:
        orm_mode = True


# Users
class UserBase(BaseModel):
    username: str
    email: str
    device_token: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    user_id: int
    created_at: datetime
    status: Optional[str]
    badges: list[BadgeBase] = []

    class Config:
        orm_mode: True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


# Posts
class PostBase(BaseModel):
    text: str
    in_reply_to_post_id: int | None = None
    latitude: Optional[float]
    longitude: Optional[float]
    user_id: int

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    post_id: int
    status: Optional[str]

    class Config:
        orm_mode = True


class PostRead(PostBase):
    post_id: int
    status: str
    created_at: datetime
    reactions: list[ReactionBase] = []

    class Config:
        orm_mode: True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


# PostReaction
class PostReactionBase(BaseModel):
    post_id: int
    reaction_id: int

    class Config:
        orm_mode = True


class PostReactionCreate(PostReactionBase):
    pass


class PostReactionRead(PostReactionBase):
    reaction_count: int


class PostByAreaRead(BaseModel):
    latitude: float
    longitude: float
    distance_in_km: int
