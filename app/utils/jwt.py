from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.schemas import schemas
from app.db_connector.db import get_db

from app.models import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expires": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(payload)

        id: str = payload.get("id")

        expiry = payload.get("expires")
        expiry_date = datetime.strptime(expiry, '%Y-%m-%d %H:%M:%S')

        if expiry_date:
            if expiry_date < datetime.utcnow():
                raise credentials_exception

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenSchema(token_type="bearer", access_token=token)
    except JWTError as e:
        print(e)
        raise credentials_exception

    return id

def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    return verify_token_access(token, credentials_exception)