from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from data.services import is_admin, create_new_event
from keyboards.admin.keyboards import add_event, cancel_button, canсel_keyboard
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
    # if not validate_name(name):
    #     await message.answer(
    #         'Что то не так с введенным именем.\n'
    #         'Имя должно состоять из цифр или '
    #         'букв русского/латинского алфавитов '
    #         'и быть не более 200 символов.'
    #     )
    #     return
    async with state.proxy() as data:
        data['name'] = name
    await NewEventStates.next()
    await message.answer("Введите дату события в формате ГГГГ-ММ-ДД",
                         reply_markup=canсel_keyboard())


async def event_date_input(message: types.Message, state: FSMContext):
    """Ввод даты события."""
    event_date = message.text
    # if not validate_birthday(birthday):
    #     await message.answer(
    #         'Что то не так с введенной датой.\n'
    #         'Сообщение дожно быть в формате ДД.ММ '
    #         '(например 13.04 или 29.02) и быть реальной датой.'
    #     )
    #     return
    async with state.proxy() as data:
        data['event_date'] = event_date
    await NewEventStates.next()
    await message.answer("Введите время события в формате ЧЧ-ММ",
                         reply_markup=canсel_keyboard())


async def event_time_input(message: types.Message, state: FSMContext):
    """Ввод времени события."""
    event_time = message.text
    # if not validate_birthday(birthday):
    #     await message.answer(
    #         'Что то не так с введенной датой.\n'
    #         'Сообщение дожно быть в формате ДД.ММ '
    #         '(например 13.04 или 29.02) и быть реальной датой.'
    #     )
    #     return
    async with state.proxy() as data:
        data['event_time'] = event_time
    await NewEventStates.next()
    await message.answer("Введите стоимость события",
                         reply_markup=canсel_keyboard())


async def event_payment_input(message: types.Message, state: FSMContext):
    """Ввод стоимости события."""
    payment = message.text
    telegram_id = message.from_user.id

    async with state.proxy() as data:
        data['payment'] = payment
        data['owner_id'] = telegram_id
        create_new_event(data)
        await message.answer("Запись создана",
                             reply_markup=menu_reply_keyboard(True))
    await state.finish()


async def cancel_add_note(message: types.Message, state: FSMContext):
    """Отмена добавления нового события."""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Операция отменена',
                             reply_markup=menu_reply_keyboard(True))
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
    dp.register_message_handler(event_payment_input,
                                state=NewEventStates.payment)
