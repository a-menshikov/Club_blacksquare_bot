from aiogram.utils import executor

from data.create_db import create_db
from handlers.admin.add_new_event import register_add_event_handlers
from handlers.admin.delete_event import register_delete_event_handlers
from handlers.admin.edit_event import register_edit_event_handlers
from handlers.admin.handlers import register_admin_handlers
from handlers.user.handlers import register_user_handlers
from loader import TECH, bot, dp, logger


async def on_startup(_):
    """Выполняется при старте бота."""
    await create_db()
    try:
        await bot.send_message(TECH, 'Бот запущен')
    except Exception:
        pass
    logger.info('Бот запущен')

register_user_handlers(dp)
register_admin_handlers(dp)
register_add_event_handlers(dp)
register_edit_event_handlers(dp)
register_delete_event_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
