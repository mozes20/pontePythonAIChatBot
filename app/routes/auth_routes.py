from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from app.dto.chat_bot_ask_dto import ChatBotAskDto
from app.db_connector.db import get_db
from app.schemas import schemas
from app.utils import jwt
from app.utils.utils import hash_pass
from app.utils.utils import verify_password
from app.models import models  # import your SQLAlchemy User model


auth_routes = APIRouter()

@auth_routes.post("/login",response_model=schemas.TokenSchema)
async def login(userdetails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == userdetails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not verify_password(userdetails.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = jwt.create_access_token(data={"id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_routes.post("/register")
async def register(user: schemas.UserCreateSchema, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = models.User(email=user.email, hashed_password=hash_pass(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user