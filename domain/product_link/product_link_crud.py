from datetime import datetime

from domain.product_link import product_link_schema
from models import ProductLink, Feed
from sqlalchemy.orm import Session


def get_product_link_list(db: Session, feed_id: int):
    return db.query(ProductLink)\
        .filter(ProductLink.feed_id == feed_id)\
        .all()


def create_product_links(db: Session,
                         product_link_creates: list[product_link_schema.ProductLinkCreate],
                         feed: Feed):
    for product_link_create in product_link_creates:
        db_product_link = ProductLink(name=product_link_create.name,
                                      url=product_link_create.url,
                                      feed=feed,
                                      create_date=datetime.now())
        db.add(db_product_link)
