from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from keyboards.user.keyboards import in_main_menu

add_event = "Добавить событие"
delete_event_button = "Удалить событие"
edit_event_button = "Редактировать событие"
cancel_button = "Отмена"
approve_button = "Подтвердить"
skip_button = "Пропустить"
skip_comment_button = "Без комментария"
clear_comment = "Очистить комментарий"


def main_admin_menu_keyboard():
    """Клавиатура регистрации."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(add_event))
    markup.add(KeyboardButton(edit_event_button))
    markup.add(KeyboardButton(delete_event_button))
    markup.add(KeyboardButton(in_main_menu))
    return markup


def canсel_keyboard():
    """Клавиатура отмены процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup


def canсel_with_skip_keyboard():
    """Клавиатура отмены процесса с возможностью скипнуть коммент."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    markup.add(KeyboardButton(skip_comment_button))
    return markup


def approve_keyboard():
    """Клавиатура подтверждения процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(approve_button))
    markup.add(KeyboardButton(cancel_button))
    return markup


def skip_keyboard():
    """Клавиатура пропуска этапа процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(skip_button))
    markup.add(KeyboardButton(cancel_button))
    return markup


def skip_with_clear_keyboard():
    """Клавиатура пропуска этапа процесса с очисткой коммента."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(clear_comment))
    markup.add(KeyboardButton(skip_button))
    markup.add(KeyboardButton(cancel_button))
    return markup
