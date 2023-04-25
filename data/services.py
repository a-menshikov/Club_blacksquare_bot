import datetime
from typing import Optional

from sqlalchemy.sql import exists

from config import delta_days_for_notification, timezone
from keyboards.user.keyboards import menu_reply_keyboard
from loader import ADMIN, bot, logger

from .db_loader import db_session
from .models import Event, User, UserNotificationStatus


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличия пользователя в базе (таблица users)."""
    check = db_session.query(exists().where(
        User.id == telegram_id)).scalar()
    if check:
        return True
    return False


def get_all_users() -> list:
    """Получить id всех пользователей."""
    all_users = db_session.query(User.id).all()
    return all_users


def fill_notifications() -> None:
    """Заполнение статусов подписки на уведомления."""
    users = get_all_users()
    for user in users:
        user_id = user[0]
        check = db_session.query(exists().where(
            UserNotificationStatus.user_id == user_id)).scalar()
        if not check:
            create_new_notification(user_id)


def is_admin(telegram_id: int) -> bool:
    """Проверка на админа."""
    return telegram_id in ADMIN


def create_new_user(telegram_id: int) -> None:
    """Создание нового пользователя"""
    new_user = User(id=telegram_id)
    db_session.add(new_user)
    db_session.commit()
    logger.info(f'Зарегистрирован новый пользователь {telegram_id}')


def create_new_event(data: dict) -> None:
    """Создание нового события"""
    new_event = Event(**data)
    db_session.add(new_event)
    db_session.commit()
    logger.info(f"{data['owner_id']} создал новое событие {data['name']}")


def create_new_notification(telegram_id: int) -> None:
    """Создание подписки на уведомления"""
    new_subscribe = UserNotificationStatus(user_id=telegram_id)
    db_session.add(new_subscribe)
    db_session.commit()
    logger.info(f'Пользователь {telegram_id} подписался на уведомления')


def delete_event(event_id: str) -> None:
    """Удаление события"""
    event = db_session.query(Event).filter(
        Event.id == event_id).one()
    db_session.delete(event)
    db_session.commit()
    logger.info(f"Удалено событие {event_id}")


def update_event(data: dict) -> None:
    """Обновление события"""
    db_session.query(Event).filter(
        Event.id == data['event_id']).update(
            {'name': data['name'],
             'event_date': data['event_date'],
             'event_time': data['event_time'],
             'payment': data['payment'],
             'complexity': data['complexity'],
             },
            synchronize_session='fetch'
            )
    db_session.commit()
    logger.info(f"Отредактировано событие {data['event_id']}")


def notification_switcher(telegram_id: int) -> bool:
    """Переключение статуса подписки на уведомления."""
    check = get_user_notification_status(telegram_id)
    if check is None:
        return False
    else:
        db_session.query(UserNotificationStatus).filter(
            UserNotificationStatus.user_id == telegram_id).update(
                {
                    'status': not check,
                },
                synchronize_session='fetch'
                )
        db_session.commit()
        logger.info(f"Пользователь {telegram_id} изменил "
                    f"статус уведомлений на {not check}")
        return True


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
            Event.payment,
            Event.complexity,
            ).where(
                Event.event_date >= today_full_date
                ).order_by(Event.event_date).all()
    else:
        return db_session.query(
            Event.id,
            Event.name,
            Event.event_date,
            Event.event_time,
            Event.payment,
            Event.complexity,
            ).order_by(Event.event_date).all()


def get_event_info(id: str) -> list:
    """Получить информацию о событии по id."""
    return db_session.query(
            Event.name,
            Event.event_date,
            Event.event_time,
            Event.payment,
            Event.complexity,
            ).where(
                Event.id == id
                ).one_or_none()


def get_user_notification_status(telegram_id: int) -> bool:
    """Получить статус подписки пользователя на уведомления."""
    status = db_session.query(
        UserNotificationStatus.status).where(
            UserNotificationStatus.user_id == telegram_id
            ).one_or_none()
    if status is None:
        return None
    if status[0]:
        return True
    return False


def get_users_for_notification() -> list[Optional[UserNotificationStatus]]:
    """Получить пользователей с подпиской на уведомления."""
    users = db_session.query(
        UserNotificationStatus).where(
            UserNotificationStatus.status == 1
            ).all()
    return users


def make_user_calendar_message(data: list) -> str:
    """Формирование сообщения календаря для юзера"""
    if not data:
        return 'Календарь пуст.'
    base_message = ''
    for i in data:
        date = convert_date_to_read_format(i[2])
        time = convert_time_to_read_format(i[3])
        add_message = (
            f'<b>Дата:</b>  {date}\n'
            f'<b>Время:</b>  {time}\n'
            f'<b>Событие:</b>  {i[1]}\n'
            f'<b>Сложность:</b>  {i[5]}\n'
            f'<b>Стоимость:</b>  {i[4]}\n\n'
            )
        base_message += add_message
    return base_message


def make_admin_calendar_message(data: list) -> str:
    """Формирование сообщения календаря для админа"""
    if not data:
        return 'Календарь пуст.\n'
    base_message = ''
    for i in data:
        date = convert_date_to_read_format(i[2])
        add_message = (
            f'<b>{i[0]}.</b>  {i[1]}  {date}\n'
            )
        base_message += add_message
    return base_message


def convert_date_to_db_format(to_convert: str):
    """Перевод даты в формат хранения для базы."""
    day, month, year = to_convert.split('.')
    return f'{year}-{month}-{day}'


def convert_date_to_read_format(to_convert: str):
    """Перевод даты в формат для вывода/ввода."""
    year, month, day = to_convert.split('-')
    return f'{day}.{month}.{year}'


def convert_time_to_db_format(to_convert: str):
    """Перевод времени в формат хранения для базы."""
    hour, minute = to_convert.split(':')
    return f'{hour}-{minute}'


def convert_time_to_read_format(to_convert: str):
    """Перевод времени в формат для вывода/ввода."""
    hour, minute = to_convert.split('-')
    return f'{hour}:{minute}'


def get_delta_date() -> datetime.date:
    """Получить дату для проверки необходимости уведомления."""
    return datetime.datetime.now(
        timezone).date() + datetime.timedelta(
        days=delta_days_for_notification)


def get_events_for_notification() -> list[Optional[Event]]:
    """Получить события для уведомлений."""
    check_date = get_delta_date()
    events = db_session.query(
        Event).where(
            Event.event_date == check_date
            ).all()
    return events


def make_notification_message(data: list[Event]) -> str:
    """Формирование сообщения для уведомлений."""
    base_message = '<b>Напоминание:</b>\n\n'
    for event in data:
        date = convert_date_to_read_format(event.event_date)
        time = convert_time_to_read_format(event.event_time)
        add_message = (
            f'<b>Дата:</b>  {date}\n'
            f'<b>Время:</b>  {time}\n'
            f'<b>Событие:</b>  {event.name}\n'
            f'<b>Сложность:</b>  {event.complexity}\n'
            f'<b>Стоимость:</b>  {event.payment}\n\n'
            )
        base_message += add_message
    base_message += ('Отключить регулярные уведомления можно в меню '
                     '"Настройка уведомлений"')
    return base_message


async def notificate() -> None:
    """Отправка уведомлений о предстоящих событиях."""
    logger.info("Запуск рассылки уведомлений")
    events = get_events_for_notification()
    if events:
        users = get_users_for_notification()
        if users:
            notification_message = make_notification_message(events)
            for user in users:
                try:
                    admin = is_admin(user.user_id)
                    await bot.send_message(
                        user.user_id, notification_message,
                        parse_mode='html',
                        reply_markup=menu_reply_keyboard(admin))
                    logger.info(f"Напоминание для {user.user_id} отправлено")
                except Exception:
                    logger.error(f"Напоминание для {user.user_id} не ушло")
    logger.info("Рассылка уведомлений завершена")
