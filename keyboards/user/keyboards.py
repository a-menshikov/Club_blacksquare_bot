from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

reg_button = "Регистрация"
calendar = "Календарь игр"
admin_menu = "Меню админа"
cancel_button = "Отмена"
in_main_menu = "В главное меню"


def reg_keyboard():
    """Клавиатура регистрации."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(reg_button))
    return markup


def menu_reply_keyboard(admin: bool = False):
    """Клавиатура главного меню юзера."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(
        KeyboardButton(calendar),
    )
    if admin:
        markup.row(
            KeyboardButton(admin_menu),
        )
    return markup
