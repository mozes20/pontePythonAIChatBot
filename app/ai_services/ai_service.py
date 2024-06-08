import openai

from app.models import models
from sqlalchemy.orm import Session


class AiService:
    def __init__(self):
        openai.api_key = 'YOUR API KEY HERE'

    def ask_gpt3(self, db: Session, chat_id, question):
        messages = self.convert_to_ai_communication_schema(self.get_last_ten_asks_by_id(chat_id, db))
        messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response['choices'][0]['message']['content']

        new_chat_element = models.AiChatBotContent(chat_id=chat_id, question=question, answer=reply)
        db.add(new_chat_element)
        db.commit()
        db.refresh(new_chat_element)
        return {"reply": reply}

    def dummy_ai(self, db: Session, chat_id, question):
        messages = self.convert_to_ai_communication_schema(self.get_last_ten_asks_by_id(chat_id, db))
        messages.append({"role": "user", "content": question})
        ## Here we can add our remote AI service call
        ## For now we will just return a dummy response
        dummy_response = f"Mock AI response to '{question}'"
        new_chat_element = models.AiChatBotContent(chat_id=chat_id, question=question, answer=dummy_response)
        db.add(new_chat_element)
        db.commit()
        db.refresh(new_chat_element)
        return {"reply": dummy_response}

    def last_asks(self, chat_id, db:Session):
        return db.query(models.AiChatBotContent).filter(models.AiChatBotContent.chat_id == chat_id).all()

    def get_last_ten_asks_by_id(self, chat_id, db: Session):
        return (db.query(models.AiChatBotContent)
                .filter(models.AiChatBotContent.chat_id == chat_id)
                .order_by(models.AiChatBotContent.id.desc()).limit(10).all())

    @staticmethod
    def convert_to_ai_communication_schema(ai_chat_bot_contents: list[models.AiChatBotContent]):
        #pre knlowledge content
        messages = [{"role": "system", "content": 'You are a intelligent assistant.'}]
        for ai_chat_bot_content in ai_chat_bot_contents:
            if ai_chat_bot_content:
                messages.append({"role": "user", "content": ai_chat_bot_content.question})
                messages.append({"role": "assistant", "content": ai_chat_bot_content.answer})
        return messages
