from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from data.services import (convert_date_to_db_format,
                           convert_date_to_read_format,
                           convert_time_to_db_format,
                           convert_time_to_read_format, create_new_event,
                           is_admin)
from handlers.admin.validators import (validate_date, validate_string_field,
                                       validate_time)
from keyboards.admin.keyboards import (add_event, approve_button,
                                       approve_keyboard, cancel_button,
                                       canсel_keyboard,
                                       canсel_with_skip_keyboard,
                                       main_admin_menu_keyboard,
                                       skip_comment_button)
from keyboards.user.keyboards import menu_reply_keyboard
from states.add_event import NewEventStates


async def new_event(message: types.Message):
    """Добавление нового события."""
    telegram_id = message.from_user.id
    admin = is_admin(telegram_id)
    if admin:
        await NewEventStates.name.set()
        await message.answer("Введите название события",
                             reply_markup=canсel_keyboard())
    else:
        await message.answer("Ты не админ. Больше так не делай.",
                             reply_markup=menu_reply_keyboard(False))


async def event_name_input(message: types.Message, state: FSMContext):
    """Ввод названия события."""
    name = message.text
    if not validate_string_field(name):
        await message.answer(
            'Что то не так с введенным текстом.\n'
            'Название не должно содержать символы <> '
            'и быть не длиннее 1000 символов.'
        )
        return
    async with state.proxy() as data:
        data['name'] = name
    await NewEventStates.next()
    await message.answer("Введите дату события в формате ДД.ММ.ГГГГ",
                         reply_markup=canсel_keyboard())


async def event_date_input(message: types.Message, state: FSMContext):
    """Ввод даты события."""
    event_date = message.text.strip()
    if not validate_date(event_date):
        await message.answer(
            'Что то не так с введенной датой.\n'
            'Сообщение дожно быть в формате ДД.ММ.ГГГГ'
            '(например 13.04.2026).'
        )
        return
    async with state.proxy() as data:
        data['event_date'] = convert_date_to_db_format(event_date)
    await NewEventStates.next()
    await message.answer("Введите время события в формате ЧЧ:ММ",
                         reply_markup=canсel_keyboard())


async def event_time_input(message: types.Message, state: FSMContext):
    """Ввод времени события."""
    event_time = message.text.strip()
    if not validate_time(event_time):
        await message.answer(
            'Что то не так с введенным временем.\n'
            'Сообщение дожно быть в формате ЧЧ:ММ '
            '(например 12:00 или 23:59).'
        )
        return
    async with state.proxy() as data:
        data['event_time'] = convert_time_to_db_format(event_time)
    await NewEventStates.next()
    await message.answer("Введите ожидаемую сложность события",
                         reply_markup=canсel_keyboard())


async def event_complexity_input(message: types.Message, state: FSMContext):
    """Ввод сложности события."""
    event_complexity = message.text.strip()
    if not validate_string_field(event_complexity):
        await message.answer(
            'Что то не так с введенной сложностью.\n'
            'Текст не должен содержать символы <> '
            'и быть не длиннее 1000 символов.'
        )
        return
    async with state.proxy() as data:
        data['complexity'] = event_complexity
    await NewEventStates.next()
    await message.answer("Введите стоимость события",
                         reply_markup=canсel_keyboard())


async def event_payment_input(message: types.Message, state: FSMContext):
    """Ввод стоимости события."""
    payment = message.text.strip()
    if not validate_string_field(payment):
        await message.answer(
            'Что то не так с введенной стоимость.\n'
            'Текст не должен содержать символы <> '
            'и быть не длиннее 1000 символов.'
        )
        return
    async with state.proxy() as data:
        data['payment'] = payment
    await NewEventStates.next()
    await message.answer("Введите комментарий к событию, или "
                         "оставьте это поле пустым.",
                         reply_markup=canсel_with_skip_keyboard())


async def event_comment_input(message: types.Message, state: FSMContext):
    """Ввод комментария к событию."""
    comment = message.text.strip()
    telegram_id = message.from_user.id

    if comment == skip_comment_button:
        comment = ''
    else:
        if not validate_string_field(comment):
            await message.answer(
                'Что то не так с комментарием.\n'
                'Текст не должен содержать символы <> '
                'и быть не длиннее 1000 символов.'
            )
            return
    async with state.proxy() as data:
        data['comment'] = comment
        data['owner_id'] = telegram_id

    read_date = convert_date_to_read_format(data['event_date'])
    read_time = convert_time_to_read_format(data['event_time'])

    check_message = (
        f"<u>Подтвердите добавление события:</u>\n\n"
        f"<b>Дата:</b> {read_date}\n"
        f"<b>Время:</b> {read_time}\n"
        f"<b>Событие:</b> {data['name']}\n"
        f"<b>Сложность:</b> {data['complexity']}\n"
        f"<b>Стоимость:</b> {data['payment']}\n"
        f"<b>Комментарий:</b> {data['comment']}"
    )

    await NewEventStates.next()

    await message.answer(check_message,
                         parse_mode='html',
                         reply_markup=approve_keyboard())


async def new_event_approve(message: types.Message, state: FSMContext):
    """Подтверждение создания события."""
    if message.text == approve_button:
        async with state.proxy() as data:
            create_new_event(data)
        await message.answer("Запись создана",
                             reply_markup=main_admin_menu_keyboard())
        await state.finish()
    else:
        await message.answer("Подтвердите или отмените процесс")
        return


async def cancel_add_note(message: types.Message, state: FSMContext):
    """Отмена добавления нового события."""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Операция отменена',
                             reply_markup=main_admin_menu_keyboard())
    else:
        await message.answer('Так ведь нечего отменять',
                             reply_markup=menu_reply_keyboard(True))


def register_add_event_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_add_note, text=cancel_button, state='*')
    dp.register_message_handler(new_event, text=add_event, state=None)
    dp.register_message_handler(event_name_input, state=NewEventStates.name)
    dp.register_message_handler(event_date_input,
                                state=NewEventStates.event_date)
    dp.register_message_handler(event_time_input,
                                state=NewEventStates.event_time)
    dp.register_message_handler(event_complexity_input,
                                state=NewEventStates.complexity)
    dp.register_message_handler(event_payment_input,
                                state=NewEventStates.payment)
    dp.register_message_handler(event_comment_input,
                                state=NewEventStates.comment)
    dp.register_message_handler(new_event_approve,
                                state=NewEventStates.approve)
