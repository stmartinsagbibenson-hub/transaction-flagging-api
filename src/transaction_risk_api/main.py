from fastapi import FastAPI
from .api import router
from .config import get_settings

settings = get_settings()
app = FastAPI(title=settings["app_name"], version="1.0.0")
app.include_router(router)