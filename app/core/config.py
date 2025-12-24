from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# 🔑 Force-load .env from project root
load_dotenv()


class Settings(BaseSettings):
    ENV: str = "dev"

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str


settings = Settings()
