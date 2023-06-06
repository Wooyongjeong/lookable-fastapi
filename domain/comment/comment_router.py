from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from database import get_db

from domain.comment import comment_schema, comment_crud
from domain.feed import feed_router
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/comment"
)


@router.post("/create/{feed_id}", status_code=status.HTTP_204_NO_CONTENT)
def comment_create(feed_id: int,
                   _comment_create: comment_schema.CommentCreate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    feed = feed_router.get_feed(db, feed_id=feed_id)
    comment_crud.create_comment(db, feed=feed,
                                comment_create=_comment_create,
                                user=current_user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def comment_update(_comment_update: comment_schema.CommentUpdate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    comment = comment_crud.get_comment(db,
                                       comment_id=_comment_update.comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='해당 댓글을 찾을 수 없습니다.')
    if comment.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='수정 권한이 없습니다.')
    comment_crud.update_comment(db, db_comment=comment,
                                comment_update=_comment_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def comment_delete(_comment_delete: comment_schema.CommentDelete,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    comment = comment_crud.get_comment(db,
                                       comment_id=_comment_delete.comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='해당 댓글을 찾을 수 없습니다.')
    if comment.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='삭제 권한이 없습니다.')
    comment_crud.delete_comment(db, db_comment=comment)
