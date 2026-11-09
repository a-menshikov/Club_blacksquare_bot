from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from data.services import (delete_event, get_calendar, get_event_card_data,
                           is_admin, make_event_buttons, make_event_card)
from keyboards.admin.keyboards import (cancel_button, canсel_keyboard,
                                       card_cb, delete_card_keyboard,
                                       delete_event_button, event_cb,
                                       events_inline_keyboard,
                                       main_admin_menu_keyboard)
from keyboards.user.keyboards import menu_reply_keyboard
from loader import logger
from states.delete_event import DeleteEventStates


async def delete_event_start(message: types.Message):
    """Начало удаления события: выбор события кнопкой."""
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ. Больше так не делай.",
                             reply_markup=menu_reply_keyboard(False))
        return
    events = get_calendar(future=True)
    if not events:
        await message.answer('Будущих событий нет.',
                             reply_markup=main_admin_menu_keyboard())
        return
    await DeleteEventStates.event_id.set()
    await message.answer('Отменить можно кнопкой «Отмена».',
                         reply_markup=canсel_keyboard())
    await message.answer(
        'Выберите событие, которое нужно удалить:',
        reply_markup=events_inline_keyboard(make_event_buttons(events)))


async def delete_event_approve(call: types.CallbackQuery, callback_data: dict,
                               state: FSMContext):
    """Событие выбрано: показать карточку и спросить подтверждение."""
    await call.answer()
    event = get_event_card_data(callback_data['id'])
    if event is None:
        await call.message.answer('Такого события уже нет.')
        return
    await state.update_data(event_id=event['event_id'])
    await DeleteEventStates.approve.set()
    await call.message.answer(
        f'<u>Подтвердите удаление события:</u>\n\n{make_event_card(event)}',
        parse_mode='html',
        reply_markup=delete_card_keyboard())


async def delete_event_finish(call: types.CallbackQuery, state: FSMContext):
    """Завершение удаления события."""
    await call.answer()
    data = await state.get_data()
    logger.info(f"{call.from_user.id} удаляет событие {data['event_id']}")
    delete_event(data['event_id'])
    await state.finish()
    await call.message.answer("Запись удалена",
                              reply_markup=main_admin_menu_keyboard())


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
    dp.register_callback_query_handler(delete_event_approve, event_cb.filter(),
                                       state=DeleteEventStates.event_id)
    dp.register_callback_query_handler(delete_event_finish,
                                       card_cb.filter(action='delete'),
                                       state=DeleteEventStates.approve)
