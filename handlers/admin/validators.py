import re
from datetime import datetime


def validate_date(message):
    """Дата события: строго ДД.ММ.ГГ и такая дата существует."""
    if not re.fullmatch(r"\d{2}\.\d{2}\.\d{2}", message):
        return False
    try:
        datetime.strptime(message, '%d.%m.%y')
    except ValueError:
        return False
    return True


def validate_time(message):
    """Время события: строго ЧЧ:ММ и такое время существует."""
    if not re.fullmatch(r"\d{2}:\d{2}", message):
        return False
    try:
        datetime.strptime(message, '%H:%M')
    except ValueError:
        return False
    return True


def validate_string_field(message):
    """Валидация введенных данных в типовое строковое поле."""
    return (re.fullmatch(
        r"^[^<>]+$",
        message
    ) and len(message) <= 1000)
