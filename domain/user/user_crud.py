from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate, UserUpdatePassword
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   create_date=datetime.now())
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def update_user_password(db: Session,
                         db_user: User,
                         user_update_password: UserUpdatePassword):
    db_user.password = pwd_context.hash(user_update_password.password1)
    db_user.update_date = datetime.now()
    db.add(db_user)
    db.commit()


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
