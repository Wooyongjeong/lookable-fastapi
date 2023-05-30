from datetime import datetime

from domain.feed.feed_schema import FeedCreate
from models import Feed, User
from sqlalchemy.orm import Session


def get_feed_list(db: Session, skip: int = 0, limit: int = 10):
    _feed_list = db.query(Feed)\
        .order_by(Feed.create_date.desc())

    total = _feed_list.count()
    feed_list = _feed_list.offset(skip).limit(limit).all()
    return total, feed_list


def get_feed(db: Session, feed_id: int):
    return db.query(Feed).get(feed_id)


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
    db.commit()
    return db_feed
