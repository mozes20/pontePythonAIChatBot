from pydantic import BaseModel


class ChatBotAskDto(BaseModel):
    text: str
