from aiogram.utils import executor
from loader import TECH, bot, dp
from data.create_db import create_db
from handlers.user.handlers import register_user_handlers
from handlers.admin.handlers import register_admin_handlers
from handlers.admin.add_new_event import register_add_event_handlers


async def on_startup(_):
    """Выполняется при старте бота."""
    await create_db()
    await bot.send_message(TECH, 'Бот запущен')

register_user_handlers(dp)
register_admin_handlers(dp)
register_add_event_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
