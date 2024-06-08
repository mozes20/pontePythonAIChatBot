from pydantic import BaseModel


class ChatBotAskDto(BaseModel):
    chat_id: int
    response: str
