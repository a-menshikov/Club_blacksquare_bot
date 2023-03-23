from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


engine = create_engine('sqlite:///db/square.db')

engine.connect()

db_session = Session(bind=engine)

Base = declarative_base()
