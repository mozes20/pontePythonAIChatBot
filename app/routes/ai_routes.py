from fastapi import APIRouter, Depends
from fastapi import Request
from app.ai_services.ai_service import AiService
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from app.dto.chat_bot_ask_dto import ChatBotAskDto
from app.db_connector.db import get_db
from app.utils.jwt import verify_token_access
from app.utils.jwt_bearer import JWTBearer
from app.utils.jwt import get_current_user_id

ai_service = AiService()
ai_routes = APIRouter()
limiter = Limiter(key_func=get_remote_address)



@ai_routes.post("/gpt-chatbot" , dependencies=[Depends(JWTBearer())])
@limiter.limit("3/minute")
async def gpt_question(request: Request, ask_gpt3: ChatBotAskDto, db: Session = Depends(get_db)):

    token = request.headers.get('Authorization').split(' ')[1]
    user_id = get_current_user_id(token, db)

    return {"Bot": ai_service.ask_gpt3(db,user_id,ask_gpt3.text), "user_id": user_id}


@ai_routes.get("/last-asks")
async def last_asks(db: Session = Depends(get_db)):
    return ai_service.last_asks(0, db)



@ai_routes.post("/mock-ai", dependencies=[Depends(JWTBearer())], )
@limiter.limit("3/minute")
async def dummy_ai(request: Request, ask_gpt3: ChatBotAskDto, db: Session = Depends(get_db)):

    token = request.headers.get('Authorization').split(' ')[1]
    user_id = get_current_user_id(token, db)

    return ai_service.dummy_ai(db, user_id, ask_gpt3.text)
