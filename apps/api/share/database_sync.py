from settings import get_settings
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

SETTINGS = get_settings()
engine = create_engine(SETTINGS.database_sync_url, echo=False)


def get_session():
    with Session(engine) as session:
        yield session
