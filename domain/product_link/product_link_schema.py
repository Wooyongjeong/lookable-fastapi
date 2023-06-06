import datetime

from pydantic import BaseModel, validator


class ProductLink(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True


class ProductLinkCreate(BaseModel):
    name: str
    url: str

    @validator('name', 'url')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
