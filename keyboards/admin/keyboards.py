from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from keyboards.user.keyboards import in_main_menu

add_event = "Добавить событие"
cancel_button = "Отмена"


def main_admin_menu_keyboard():
    """Клавиатура регистрации."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(add_event))
    markup.add(KeyboardButton(in_main_menu))
    return markup


def canсel_keyboard():
    """Клавиатура отмены процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup
