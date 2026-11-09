import asyncio

import aioschedule
from aiogram.utils import executor

from data.create_db import create_db
from data.db_loader import db_session
from data.sender import send_message_with_retry
from data.services import notificate
from handlers.admin.add_new_event import register_add_event_handlers
from handlers.admin.delete_event import register_delete_event_handlers
from handlers.admin.edit_event import register_edit_event_handlers
from handlers.admin.handlers import register_admin_handlers
from handlers.admin.own_game_distrib import register_own_game_distribution_handlers
from handlers.user.handlers import register_user_handlers
from loader import TECH, dp, logger


async def on_startup(_):
    """Выполняется при старте бота."""
    await create_db()
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    try:
        await send_message_with_retry(TECH, 'Бот запущен')
    except Exception:
        pass  # причина уже в логе; без этого сообщения бот работает
    logger.info('Бот запущен')


async def scheduler():
    """Расписание выполнения задач."""
    scheduler = aioschedule.Scheduler()
    scheduler.every().day.at("09:00").do(notificate)
    while True:
        await scheduler.run_pending()
        await asyncio.sleep(1)


async def on_handler_error(update, exception):
    """Сбой в обработчике: в лог и откат сеанса базы, он один на весь бот."""
    logger.error(f'Сбой при обработке сообщения: {exception!r}',
                 exc_info=exception)
    db_session.rollback()
    return True


register_user_handlers(dp)
register_admin_handlers(dp)
register_add_event_handlers(dp)
register_edit_event_handlers(dp)
register_delete_event_handlers(dp)
register_own_game_distribution_handlers(dp)
dp.register_errors_handler(on_handler_error)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
