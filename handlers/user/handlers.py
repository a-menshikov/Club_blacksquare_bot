from aiogram import types
from aiogram.dispatcher import Dispatcher

from data.services import (create_new_user, get_calendar, is_admin,
                           is_user_exist_in_base, make_user_calendar_message)
from keyboards.user.keyboards import (calendar, in_main_menu,
                                      menu_reply_keyboard, reg_button,
                                      reg_keyboard)


async def starter(message: types.Message):
    """Ответы на команды start и help"""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    admin = is_admin(telegram_id)
    if checker:
        await message.answer("Привет. Этот бот СКИТ Чёрный квадрат.",
                             reply_markup=menu_reply_keyboard(admin))
    else:
        await message.answer("Привет. Этот бот СКИТ Чёрный квадрат.\n"
                             "Ты здесь впервые. Жми кнопку и начнём.",
                             reply_markup=reg_keyboard())


async def main_menu(message: types.Message):
    """В главное меню."""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    admin = is_admin(telegram_id)
    if checker:
        await message.answer("Меню:",
                             reply_markup=menu_reply_keyboard(admin))
    else:
        await message.answer("Привет. Этот бот СКИТ Чёрный квадрат.\n"
                             "Ты здесь впервые. Жми кнопку и начнём.",
                             reply_markup=reg_keyboard())


async def registration(message: types.Message):
    """Регистрация нового пользователя."""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    admin = is_admin(telegram_id)
    if checker:
        await message.answer("Вы уже зарегистрированы. Воспользуйтесь меню",
                             reply_markup=menu_reply_keyboard(admin))
    else:
        create_new_user(telegram_id)
        await message.answer("Welcome. Полный функционал доступен."
                             " Воспользуйтесь меню",
                             reply_markup=menu_reply_keyboard(admin))


async def get_future_calendar(message: types.Message):
    """Получить календарь будущих игр."""
    telegram_id = message.from_user.id
    admin = is_admin(telegram_id)
    data = get_calendar(future=True)
    events_message = make_user_calendar_message(data)
    await message.answer(events_message,
                         parse_mode='html',
                         reply_markup=menu_reply_keyboard(admin))


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(starter, commands=["start", "help"])
    dp.register_message_handler(main_menu, text=in_main_menu)
    dp.register_message_handler(registration, text=reg_button)
    dp.register_message_handler(get_future_calendar, text=calendar)
