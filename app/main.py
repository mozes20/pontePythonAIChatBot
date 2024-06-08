from fastapi import FastAPI
from app.routes import ai_routes
from app.db_connector.db import engine
from app.models import models
from app.routes import auth_routes

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

#database table creation syncronise structure
models.Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

# FastAPI instance
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# include ai_routes in the app
app.include_router(ai_routes.ai_routes, prefix="/ai")
app.include_router(auth_routes.auth_routes, prefix="/auth")