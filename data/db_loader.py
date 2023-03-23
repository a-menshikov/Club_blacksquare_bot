from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///db/birthday.db')

engine.connect()

db_session = Session(bind=engine)

Base = declarative_base()


async def create_db():
    """Создание БД и наполнение ее предустановленными данными."""
    Base.metadata.create_all(engine)
