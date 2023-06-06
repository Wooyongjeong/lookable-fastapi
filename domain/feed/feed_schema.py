import datetime

from pydantic import BaseModel, validator

from domain.product_link.product_link_schema \
    import ProductLinkCreate
    import ProductLinkCreate, ProductLink
from domain.user.user_schema import User


class FeedDetail(BaseModel):
    id: int
    img: str | None = None
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    weather: str
    temperature: str
    sensitivity: str
    city: str
    district: str
    user: User
    feed_liker: list[User] = []

    class Config:
        orm_mode = True


class FeedCreate(BaseModel):
    img: str | None = None
    content: str
    weather: str
    temperature: str
    sensitivity: str
    city: str
    district: str
    product_links: list[ProductLinkCreate] = []

    @validator('content', 'weather', 'temperature', 'sensitivity',
               'city', 'district')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class Feed(BaseModel):
    id: int
    img: str | None = None
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    user: User
    feed_liker: list[User] = []
    product_links: list[ProductLink] = []

    class Config:
        orm_mode = True


class FeedList(BaseModel):
    total: int = 0
    feed_list: list[Feed] = []


class FeedUpdate(FeedCreate):
    feed_id: int


class FeedDelete(BaseModel):
    feed_id: int


class FeedLike(BaseModel):
    feed_id: int
