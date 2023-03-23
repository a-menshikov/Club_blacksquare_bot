from aiogram.utils import executor
from loader import ADMIN, bot, dp
from data.create_db import create_db
from handlers.user.handlers import register_user_handlers


async def on_startup(_):
    """Выполняется при старте бота."""
    await create_db()

    for tg_id in ADMIN:
        await bot.send_message(tg_id, 'Бот запущен')

register_user_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
