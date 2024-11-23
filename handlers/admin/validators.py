import re


def validate_date(message):
    """Валидация введенных данных в дате события."""
    return re.fullmatch(r"^[01-9]{2}.[01-9]{2}.[01-9]{4}$", message)


def validate_time(message):
    """Валидация введенных данных во времени события."""
    return re.fullmatch(r"^[01-9]{2}:[01-9]{2}$", message)


def validate_string_field(message):
    """Валидация введенных данных в типовое строковое поле."""
    return (re.fullmatch(
        r"^[^<>]+$",
        message
    ) and len(message) <= 1000)
