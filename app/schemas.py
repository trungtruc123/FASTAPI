"""
----------------------------------------------------
Schemas to communication with frontend (request, response)
- inspect data, types that send to server

"""
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class UserShow(BaseModel):
    email: EmailStr
    id: int
    create_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    context: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    create_at: datetime
    owner_id: int
    owner: UserShow

    class Config:
        # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class PostOut(BaseModel):
    Post: Post
    number_votes: int

    class Config:
        orm_mode = True
