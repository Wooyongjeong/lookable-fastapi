from datetime import datetime

from domain.feed.feed_schema import FeedCreate
from models import Feed, User
from domain.product_link import product_link_crud
from sqlalchemy.orm import Session


def get_feed_list(db: Session,
                  weather: str, temperature: str,
                  city: str, district: str,
                  skip: int = 0, limit: int = 10):
    _feed_list = db.query(Feed)\
        .join(ProductLink)\
        .join(Comment)\
        .filter(
            (Feed.weather == weather) &
            (Feed.temperature == temperature) &
            (Feed.city == city) &
            (Feed.district == district)
        )\
        .order_by(Feed.create_date.desc())

    total = _feed_list.count()
    feed_list = _feed_list.offset(skip).limit(limit).all()
    return total, feed_list


def get_feed(db: Session, feed_id: int):
    return db.query(Feed)\
        .filter(Feed.id == feed_id)\
        .first()


def create_feed(db: Session, feed_create: FeedCreate, user: User):
    db_feed = Feed(img=feed_create.img,
                   content=feed_create.content,
                   weather=feed_create.weather,
                   temperature=feed_create.temperature,
                   sensitivity=feed_create.sensitivity,
                   city=feed_create.city,
                   district=feed_create.district,
                   user=user,
                   create_date=datetime.now())
    db.add(db_feed)
    product_link_crud.create_product_links(db,
                                           product_link_creates=feed_create.product_links,
                                           feed=db_feed)
    db.commit()
    db.commit()
