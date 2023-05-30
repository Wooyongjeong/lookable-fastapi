from datetime import datetime

from domain.product_link.product_link_schema \
    import ProductLinkCreate
from models import ProductLink, Feed
from sqlalchemy.orm import Session


def get_product_link_list(db: Session, feed_id: int):
    return db.query(ProductLink)\
        .filter(ProductLink.feed_id == feed_id)\
        .all()


def create_product_links(db: Session,
                         product_link_creates: list[ProductLinkCreate],
                         feed: Feed):
    for product_link_create in product_link_creates:
        db_product_link = ProductLink(name=product_link_create.name,
                                      link=product_link_create.link,
                                      feed=feed,
                                      created_date=datetime.now())
        db.add(db_product_link)
    db.commit()
