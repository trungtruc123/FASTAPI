from fastapi import FastAPI, HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    tags=["Authentications"]
)


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''
            {
                username: "truccobelolem",
                password: 123
            }
    '''

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")

    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"token": access_token}
