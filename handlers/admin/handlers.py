from aiogram import types
from aiogram.dispatcher import Dispatcher

from data.services import is_admin
from keyboards.admin.keyboards import main_admin_menu_keyboard
from keyboards.user.keyboards import admin_menu, menu_reply_keyboard


async def admin_main_menu(message: types.Message):
    """Меню админа"""
    telegram_id = message.from_user.id
    admin = is_admin(telegram_id)
    if admin:
        await message.answer("Меню администратора",
                             reply_markup=main_admin_menu_keyboard())
    else:
        await message.answer("Ты не админ. Больше так не делай",
                             reply_markup=menu_reply_keyboard(admin))


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_main_menu, text=admin_menu)
