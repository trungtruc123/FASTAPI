from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",  # + "/id" => "/posts/id"
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" Post not found!")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()  # vote has exists
    if vote.dir == 1:
        # add vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.email} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote successful!"}
    else:
        # delete vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" Vote does not exist.")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Delete vote successful!"}
