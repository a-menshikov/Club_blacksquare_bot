from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from data.services import (get_calendar, get_event_info, is_admin,
                           make_admin_calendar_message, update_event)
from handlers.admin.validators import (validate_date, validate_name,
                                       validate_payment, validate_time)
from keyboards.admin.keyboards import (approve_button, approve_keyboard,
                                       cancel_button, canсel_keyboard,
                                       edit_event_button,
                                       main_admin_menu_keyboard, skip_button,
                                       skip_keyboard)
from keyboards.user.keyboards import menu_reply_keyboard
from loader import logger
from states.edit_event import EditEventStates


async def edit_event(message: types.Message):
    """Редактирование события."""
    telegram_id = message.from_user.id
    admin = is_admin(telegram_id)
    if admin:
        await EditEventStates.event_id.set()
        data = get_calendar(future=True)
        events_message = make_admin_calendar_message(data)
        base_message = ('\nВведите идентификатор события, '
                        'которое нужно отредактировать. Выше список '
                        'актуальных событий с идентификаторами')
        events_message += base_message
        await message.answer(events_message,
                             parse_mode='html',
                             reply_markup=canсel_keyboard())
    else:
        await message.answer("Ты не админ. Больше так не делай.",
                             reply_markup=menu_reply_keyboard(False))


async def edit_event_id(message: types.Message, state: FSMContext):
    """Получение id редактируемого события и информации о нем."""
    event_id = message.text.strip()
    data = get_event_info(event_id)
    if data:
        async with state.proxy() as payload:
            payload['event'] = data
            payload['event_id'] = event_id
            old_name = payload['event'][0]
            await EditEventStates.next()
            await message.answer((f'Текущее название: {old_name}\n'
                                  f'Введите новое название или нажмите кнопку '
                                  f'Пропустить, если поле не '
                                  f'нужно редактировать'),
                                 reply_markup=skip_keyboard()
                                 )
    else:
        check_message = 'Такого события нет. Проверьте введённый идентификатор'
        await message.answer(check_message,
                             reply_markup=canсel_keyboard())
        return


async def event_name_edit(message: types.Message, state: FSMContext):
    """Ввод нового названия события."""
    name = message.text
    if name == skip_button:
        async with state.proxy() as payload:
            payload['name'] = payload['event'][0]
            old_date = payload['event'][1]
            await EditEventStates.next()
            await message.answer((f'Текущая дата: {old_date}\n'
                                  f'Введите новую дату или нажмите кнопку '
                                  f'Пропустить, если поле не '
                                  f'нужно редактировать'),
                                 reply_markup=skip_keyboard()
                                 )
    else:
        if not validate_name(name):
            await message.answer(
                'Что то не так с введенным текстом.\n'
                'Название не должно содержать символы <> '
                'и быть не длиннее 1000 символов.'
            )
            return
        async with state.proxy() as payload:
            payload['name'] = name
            old_date = payload['event'][1]
            await EditEventStates.next()
            await message.answer((f'Текущая дата: {old_date}\n'
                                  f'Введите новую дату или нажмите кнопку '
                                  f'Пропустить, если поле не '
                                  f'нужно редактировать'),
                                 reply_markup=skip_keyboard()
                                 )


async def event_date_edit(message: types.Message, state: FSMContext):
    """Ввод новой даты события."""
    event_date = message.text
    if event_date == skip_button:
        async with state.proxy() as payload:
            payload['event_date'] = payload['event'][1]
            old_time = payload['event'][2]
            await EditEventStates.next()
            await message.answer((f'Текущее время: {old_time}\n'
                                  f'Введите новое время или нажмите кнопку '
                                  f'Пропустить, если поле не '
                                  f'нужно редактировать'),
                                 reply_markup=skip_keyboard()
                                 )
    else:
        if not validate_date(event_date):
            await message.answer(
                'Что то не так с введенной датой.\n'
                'Сообщение дожно быть в формате ГГГГ-ММ-ДД '
                '(например 2026-04-13).'
                )
            return
        async with state.proxy() as payload:
            payload['event_date'] = event_date
            old_time = payload['event'][2]
            await EditEventStates.next()
            await message.answer((f'Текущее время: {old_time}\n'
                                  f'Введите новое время или нажмите кнопку '
                                  f'Пропустить, если поле не '
                                  f'нужно редактировать'),
                                 reply_markup=skip_keyboard()
                                 )


async def event_time_edit(message: types.Message, state: FSMContext):
    """Ввод нового времени события."""
    event_time = message.text
    if event_time == skip_button:
        async with state.proxy() as payload:
            payload['event_time'] = payload['event'][2]
            old_payment = payload['event'][3]
            await EditEventStates.next()
            await message.answer((f'Текущая стоимость: {old_payment}\n'
                                  f'Введите новую стоимость или нажмите '
                                  f'кнопку Пропустить, если поле не '
                                  f'нужно редактировать'),
                                 reply_markup=skip_keyboard()
                                 )
    else:
        if not validate_time(event_time):
            await message.answer(
                'Что то не так с введенным временем.\n'
                'Сообщение дожно быть в формате ЧЧ-ММ '
                '(например 12-00 или 23-59).'
            )
            return
        async with state.proxy() as payload:
            payload['event_time'] = event_time
            old_payment = payload['event'][3]
            await EditEventStates.next()
            await message.answer((f'Текущая стоимость: {old_payment}\n'
                                  f'Введите новую стоимость или нажмите '
                                  f'кнопку Пропустить, если поле не '
                                  f'нужно редактировать'),
                                 reply_markup=skip_keyboard()
                                 )


async def event_payment_edit(message: types.Message, state: FSMContext):
    """Ввод новой стоимости события."""
    payment = message.text
    if payment == skip_button:
        async with state.proxy() as payload:
            payload['payment'] = payload['event'][3]
            await EditEventStates.next()
            check_message = (f"<u>Подтвердите редактирование события:</u>\n\n"
                             f"<b>Дата:</b> {payload['event_date']}\n"
                             f"<b>Время:</b> {payload['event_time']}\n"
                             f"<b>Событие:</b> {payload['name']}\n"
                             f"<b>Стоимость:</b> {payload['payment']}")
            await message.answer(check_message,
                                 parse_mode='html',
                                 reply_markup=approve_keyboard())
    else:
        if not validate_payment(payment):
            await message.answer(
                'Что то не так с введенной стоимость.\n'
                'Текст не должен содержать символы <> '
                'и быть не длиннее 1000 символов.'
            )
            return
        async with state.proxy() as payload:
            payload['payment'] = payment
            await EditEventStates.next()
            check_message = (f"<u>Подтвердите редактирование события:</u>\n\n"
                             f"<b>Дата:</b> {payload['event_date']}\n"
                             f"<b>Время:</b> {payload['event_time']}\n"
                             f"<b>Событие:</b> {payload['name']}\n"
                             f"<b>Стоимость:</b> {payload['payment']}")
            await message.answer(check_message,
                                 parse_mode='html',
                                 reply_markup=approve_keyboard())


async def edit_event_approve(message: types.Message, state: FSMContext):
    """Подтверждение редактирования события."""
    if message.text == approve_button:
        async with state.proxy() as payload:
            logger.info(f"{message.from_user.id} редактирует "
                        f"событие {payload['event_id']}")
            update_event(payload)
        await message.answer("Запись отредактирована",
                             reply_markup=main_admin_menu_keyboard())
        await state.finish()
    else:
        await message.answer("Подтвердите или отмените процесс")
        return


async def cancel_edit_note(message: types.Message, state: FSMContext):
    """Отмена добавления нового события."""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Операция отменена',
                             reply_markup=main_admin_menu_keyboard())
    else:
        await message.answer('Так ведь нечего отменять',
                             reply_markup=menu_reply_keyboard(True))


def register_edit_event_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_edit_note, text=cancel_button,
                                state='*')
    dp.register_message_handler(edit_event, text=edit_event_button, state=None)
    dp.register_message_handler(edit_event_id, state=EditEventStates.event_id)
    dp.register_message_handler(event_name_edit, state=EditEventStates.name)
    dp.register_message_handler(event_date_edit,
                                state=EditEventStates.event_date)
    dp.register_message_handler(event_time_edit,
                                state=EditEventStates.event_time)
    dp.register_message_handler(event_payment_edit,
                                state=EditEventStates.payment)
    dp.register_message_handler(edit_event_approve,
                                state=EditEventStates.approve)
