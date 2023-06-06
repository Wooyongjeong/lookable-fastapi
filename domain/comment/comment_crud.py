from datetime import datetime

from domain.comment.comment_schema import CommentCreate, CommentUpdate
from models import Feed, Comment, User
from sqlalchemy.orm import Session


def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()


def create_comment(db: Session, feed: Feed, user: User,
                   comment_create: CommentCreate):
    db_comment = Comment(content=comment_create.content,
                         feed=feed,
                         user=user,
                         create_date=datetime.now())
    db.add(db_comment)
    db.commit()


def update_comment(db: Session, db_comment: Comment,
                   comment_update: CommentUpdate):
    db_comment.content = comment_update.content
    db_comment.modify_date = datetime.now()
    db.add(db_comment)
    db.commit()


def delete_comment(db: Session, db_comment: Comment):
    db.delete(db_comment)
    db.commit()
