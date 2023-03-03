from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix="/posts",  # + "/id" => "/posts/id"
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # my_posts = db.query(models.Post).all()
    # search follow title
    my_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return my_posts


@router.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, context=post.context, published=post.published)
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": new_post}


@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} not found.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f" Not authorized to perform requested action")
    return post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} not found.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f" Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} not exists.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f" Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
