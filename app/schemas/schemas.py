from typing import Optional

from pydantic import BaseModel


class AiChatBotContentSchema(BaseModel):
    id: int
    chat_id: int
    question: str
    answer: str


class AiChatBotContentCreateSchema(BaseModel):
    chat_id: int
    question: str
    answer: str


class UserSchema(BaseModel):
    id: int
    email: str
    hashed_password: str


class UserCreateSchema(BaseModel):
    email: str
    password: str


class UserLoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    id: Optional[int] = None
