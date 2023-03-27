from sqlalchemy.sql import exists
import datetime
from config import timezone

from .db_loader import db_session
from .models import User, Event
from loader import ADMIN


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличия пользователя в базе (таблица users)."""
    check = db_session.query(exists().where(
        User.id == telegram_id)).scalar()
    if check:
        return True
    return False


def is_admin(telegram_id: int) -> bool:
    """Проверка на админа."""
    return telegram_id in ADMIN


def create_new_user(telegram_id: int) -> None:
    """Создание нового пользователя"""
    new_user = User(id=telegram_id)
    db_session.add(new_user)
    db_session.commit()


def create_new_event(data: dict) -> None:
    """Создание нового пользователя"""
    new_event = Event(**data)
    db_session.add(new_event)
    db_session.commit()


def get_calendar(future: bool = False) -> list:
    """Получить список событий.
    Eсли future==True - только будущие."""
    if future:
        today_full_date = datetime.datetime.now(timezone).date()
        return db_session.query(
            Event.id,
            Event.name,
            Event.event_date,
            Event.event_time,
            Event.payment
            ).where(
                Event.event_date >= today_full_date
                ).order_by(Event.event_date).all()
    else:
        return db_session.query(
            Event.id,
            Event.name,
            Event.event_date,
            Event.event_time,
            Event.payment
            ).order_by(Event.event_date).all()


def make_user_calendar_message(data: list) -> str:
    """Формирование сообщения календаря"""
    if not data:
        return 'Календарь пуст.'
    base_message = ''
    for i in data:
        add_message = (
            f'<b>Дата:</b>  {i[2]}\n'
            f'<b>Время:</b>  {i[3]}\n'
            f'<b>Событие:</b>  {i[1]}\n'
            f'<b>Стоимость:</b>  {i[4]}\n\n'
            )
        base_message += add_message
    return base_message
