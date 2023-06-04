from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from database import get_db
from domain.product_link import product_link_crud
from domain.feed import feed_schema, feed_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/feed"
)


@router.get("/list", response_model=feed_schema.FeedList)
def feed_list(weather: str, temperature: str,
              city: str, district: str,
              db: Session = Depends(get_db),
              page: int = 0, size: int = 10):
    total, _feed_list = feed_crud.get_feed_list(
        db,
        weather=weather, temperature=temperature,
        city=city, district=district,
        skip=page * size, limit=size
    )
    return {
        'total': total,
        'feed_list': _feed_list
    }


@router.get("/detail/{feed_id}", response_model=feed_schema.FeedDetail)
def feed_detail(feed_id: int, db: Session = Depends(get_db)):
    return feed_crud.get_feed(db, feed_id=feed_id)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def feed_create(_feed_create: feed_schema.FeedCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    feed = feed_crud.create_feed(db, feed_create=_feed_create,
                                 user=current_user)
    product_link_crud.create_product_links(db,
                                           product_link_creates=_feed_create.product_links,
                                           feed=feed)


@router.put("/update/{feed_id}", status_code=status.HTTP_204_NO_CONTENT)
def feed_update(_feed_update: feed_schema.FeedUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    feed_crud.update_feed(db, feed_update=_feed_update, user=current_user)
