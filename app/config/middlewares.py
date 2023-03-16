from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import getSettings

settings = getSettings()


def init_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
        allow_origins=settings.ORIGINS
    )