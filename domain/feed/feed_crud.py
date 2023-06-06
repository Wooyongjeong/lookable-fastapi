from datetime import datetime

from domain.product_link import product_link_crud
from domain.feed.feed_schema import FeedCreate, FeedUpdate
from models import Feed, User, ProductLink, Comment
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


def update_feed(db: Session, db_feed: Feed,
                feed_update: FeedUpdate):
    db_feed.img = feed_update.img
    db_feed.content = feed_update.content
    db_feed.weather = feed_update.weather
    db_feed.temperature = feed_update.temperature
    db_feed.sensitivity = feed_update.sensitivity
    db_feed.city = feed_update.city
    db_feed.district = feed_update.district
    db_feed.product_links = product_link_crud.update_feed_product_links(db,
                                                                        product_links=feed_update.product_links)
    db_feed.modify_date = datetime.now()

    db.add(db_feed)
    db.commit()


def delete_feed(db: Session, db_feed: Feed):
    db.delete(db_feed)
    db.commit()
    db.commit()
