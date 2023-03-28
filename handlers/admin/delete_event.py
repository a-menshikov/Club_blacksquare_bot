from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from data.services import (delete_event, get_calendar, get_event_info,
                           is_admin, make_admin_calendar_message)
from keyboards.admin.keyboards import (approve_button, approve_keyboard,
                                       cancel_button, canсel_keyboard,
                                       delete_event_button,
                                       main_admin_menu_keyboard)
from keyboards.user.keyboards import menu_reply_keyboard
from loader import logger
from states.delete_event import DeleteEventStates


async def delete_event_start(message: types.Message):
    """Начало удаления события."""
    telegram_id = message.from_user.id
    admin = is_admin(telegram_id)
    if admin:
        await DeleteEventStates.event_id.set()
        data = get_calendar(future=True)
        events_message = make_admin_calendar_message(data)
        base_message = ('\nВведите идентификатор события, '
                        'которое нужно удалить. Выше список '
                        'актуальных событий с идентификаторами')
        events_message += base_message
        await message.answer(events_message,
                             parse_mode='html',
                             reply_markup=canсel_keyboard())
    else:
        await message.answer("Ты не админ. Больше так не делай.",
                             reply_markup=menu_reply_keyboard(False))


async def delete_event_approve(message: types.Message, state: FSMContext):
    """Подтверждение удаления события."""
    event_id = message.text.strip()
    data = get_event_info(event_id)
    if data:
        check_message = (f"<u>Подтвердите удаление события:</u>\n\n"
                         f"<b>Дата:</b> {data[1]}\n"
                         f"<b>Время:</b> {data[2]}\n"
                         f"<b>Событие:</b> {data[0]}\n"
                         f"<b>Стоимость:</b> {data[3]}")
        async with state.proxy() as payload:
            payload['event_id'] = event_id
        await DeleteEventStates.next()
        await message.answer(check_message,
                             parse_mode='html',
                             reply_markup=approve_keyboard())
    else:
        check_message = 'Такого события нет. Проверьте введённый идентификатор'
        await message.answer(check_message,
                             reply_markup=canсel_keyboard())
        return


async def delete_event_finish(message: types.Message, state: FSMContext):
    """Завершение удаления события."""
    if message.text == approve_button:
        async with state.proxy() as payload:
            logger.info(f"{message.from_user.id} удаляет "
                        f"событие {payload['event_id']}")
            delete_event(payload['event_id'])
        await message.answer("Запись удалена",
                             reply_markup=main_admin_menu_keyboard())
        await state.finish()
    else:
        await message.answer("Подтвердите или отмените процесс")
        return


async def cancel_add_note(message: types.Message, state: FSMContext):
    """Отмена удаления события."""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Операция отменена',
                             reply_markup=main_admin_menu_keyboard())
    else:
        await message.answer('Так ведь нечего отменять',
                             reply_markup=menu_reply_keyboard(True))


def register_delete_event_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_add_note, text=cancel_button, state='*')
    dp.register_message_handler(delete_event_start, text=delete_event_button,
                                state=None)
    dp.register_message_handler(delete_event_approve,
                                state=DeleteEventStates.event_id)
    dp.register_message_handler(delete_event_finish,
                                state=DeleteEventStates.approve)
