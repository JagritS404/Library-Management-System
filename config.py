from pydantic import BaseSettings


class Settings(BaseSettings):
DATABASE_URL: str = "sqlite:///./library.db"
JWT_SECRET: str
JWT_ALGORITHM: str = "HS256"
JWT_EXPIRE_MINUTES: int = 60 * 24
GOOGLE_CLIENT_ID: str = ""
GOOGLE_CLIENT_SECRET: str = ""
EMAIL_HOST: str = ""
EMAIL_PORT: int = 587
EMAIL_USER: str = ""
EMAIL_PASS: str = ""


class Config:
env_file = ".env"


settings = Settings()