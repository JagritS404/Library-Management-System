from sqlmodel import SQLModel, create_engine, Session
from config import settings


engine = create_engine(settings.DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db():
from app.models.models import * # noqa: F401
SQLModel.metadata.create_all(engine)


def get_session():
with Session(engine) as session:
yield session