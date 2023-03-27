import re


def validate_name(message):
    """Валидация введенных данных в названии события."""
    return (re.fullmatch(
        r"^[^<>]+$",
        message
    ) and len(message) <= 1000)


def validate_date(message):
    """Валидация введенных данных в дате события."""
    return re.fullmatch(r"^[01-9]{4}-[01-9]{2}-[01-9]{2}$", message)


def validate_time(message):
    """Валидация введенных данных во времени события."""
    return re.fullmatch(r"^[01-9]{2}-[01-9]{2}$", message)


def validate_payment(message):
    """Валидация введенных данных в стоимости события."""
    return (re.fullmatch(
        r"^[^<>]+$",
        message
    ) and len(message) <= 1000)
