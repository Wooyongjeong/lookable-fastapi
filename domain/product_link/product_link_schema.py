import datetime

from pydantic import BaseModel, validator


class ProductLink(BaseModel):
    name: str
    link: str
    feed_id: int

    class Config:
        orm_mode = True


class ProductLinkCreate(BaseModel):
    name: str
    link: str

    @validator('name', 'link')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
