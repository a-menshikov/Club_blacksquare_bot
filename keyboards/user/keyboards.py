from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

reg_button = "Регистрация"
calendar = "Календарь игр"
notification = "Настройка уведомлений"
yes_notification = "Уведомлять"
no_notification = "Не уведомлять"
admin_menu = "Меню админа"
cancel_button = "Отмена"
in_main_menu = "В главное меню"


def reg_keyboard():
    """Клавиатура регистрации."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(reg_button))
    return markup


def notification_keyboard(check: bool):
    """Клавиатура настройки уведомлений."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if check:
        markup.add(KeyboardButton(no_notification))
    else:
        markup.add(KeyboardButton(yes_notification))
    markup.add(KeyboardButton(in_main_menu))
    return markup


def menu_reply_keyboard(admin: bool = False):
    """Клавиатура главного меню юзера."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(
        KeyboardButton(calendar),
        KeyboardButton(notification),
    )
    if admin:
        markup.row(
            KeyboardButton(admin_menu),
        )
    return markup
