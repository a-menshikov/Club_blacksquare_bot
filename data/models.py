from datetime import date

from sqlalchemy import Column, ForeignKey, Integer, Text

from .db_loader import Base


class User(Base):
    """Модель пользователя."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    created_on = Column(Text, default=date.today)


class Event(Base):
    """Модель события."""
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Text, nullable=False)
    event_date = Column(Text, nullable=False)
    event_time = Column(Text, nullable=False)
    complexity = Column(Text, nullable=False)
    payment = Column(Text, nullable=False)
    created_on = Column(Text, default=date.today)
