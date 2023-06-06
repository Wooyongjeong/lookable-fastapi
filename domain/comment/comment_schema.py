import datetime

from pydantic import BaseModel, validator

from domain.user.user_schema import User


class Comment(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    user: User
    liker: list[User] = []

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class CommentList(BaseModel):
    total: int = 0
    comment_list: list[Comment] = []


class CommentUpdate(CommentCreate):
    comment_id: int


class CommentDelete(BaseModel):
    comment_id: int
