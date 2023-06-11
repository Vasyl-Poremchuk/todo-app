from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    The function creates and closes a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
