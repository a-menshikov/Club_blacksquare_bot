from aiogram.utils import executor
from loader import ADMIN, bot, dp
from data.db_loader import create_db


async def on_startup(_):
    """Выполняется при старте бота."""

    for tg_id in ADMIN:
        await create_db()
        await bot.send_message(tg_id, 'Бот запущен')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
