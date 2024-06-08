from app.db_connector.db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text


class AiChatBotContent(Base):
    __tablename__ = "ai_chat_bot_content"

    id = Column(Integer,primary_key=True,nullable=False)
    chat_id = Column(Integer,nullable=False)
    question = Column(String,nullable=False)
    answer = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
