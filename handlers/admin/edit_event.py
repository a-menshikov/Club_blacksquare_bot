from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from data.services import (convert_date_to_db_format,
                           convert_date_to_read_format,
                           convert_time_to_db_format,
                           convert_time_to_read_format, get_calendar,
                           get_event_card_data, is_admin, make_event_buttons,
                           make_event_card, update_event)
from handlers.admin.validators import (validate_date, validate_string_field,
                                       validate_time)
from keyboards.admin.keyboards import (EVENT_FIELD_BUTTONS, cancel_button,
                                       canсel_keyboard, card_cb, clear_comment,
                                       edit_event_button, event_card_keyboard,
                                       event_cb, events_inline_keyboard,
                                       field_cb, main_admin_menu_keyboard,
                                       skip_button, skip_keyboard,
                                       skip_with_clear_keyboard,
                                       skip_with_default_time_button_keyboard)
from keyboards.user.keyboards import menu_reply_keyboard
from states.edit_event import EditEventStates


async def edit_event_start(message: types.Message):
    """Редактирование события: выбор события кнопкой."""
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ. Больше так не делай.",
                             reply_markup=menu_reply_keyboard(False))
        return
    events = get_calendar(future=True)
    if not events:
        await message.answer('Будущих событий нет.',
                             reply_markup=main_admin_menu_keyboard())
        return
    await EditEventStates.choose_event.set()
    await message.answer('Отменить можно кнопкой «Отмена».',
                         reply_markup=canсel_keyboard())
    await message.answer(
        'Выберите событие для редактирования:',
        reply_markup=events_inline_keyboard(make_event_buttons(events)))


async def event_chosen(call: types.CallbackQuery, callback_data: dict,
                       state: FSMContext):
    """Событие выбрано: показать карточку."""
    await call.answer()
    event = get_event_card_data(callback_data['id'])
    if event is None:
        await call.message.answer('Такого события уже нет.')
        return
    await state.update_data(**event)
    await show_card(call.message, state)


async def show_card(message: types.Message, state: FSMContext):
    """Карточка события с кнопками полей."""
    data = await state.get_data()
    await EditEventStates.card.set()
    await message.answer(
        '<u>Редактирование. Выберите поле или сохраните:</u>\n\n'
        f'{make_event_card(data)}',
        parse_mode='html',
        reply_markup=event_card_keyboard())


async def field_chosen(call: types.CallbackQuery, callback_data: dict,
                       state: FSMContext):
    """Поле карточки выбрано: спросить новое значение."""
    await call.answer()
    field = callback_data['name']
    data = await state.get_data()
    current = data[field]
    hint = ''
    keyboard = skip_keyboard()
    if field == 'event_date':
        current = convert_date_to_read_format(current)
        hint = ' в формате ДД.ММ.ГГ'
    elif field == 'event_time':
        current = convert_time_to_read_format(current)
        hint = ' в формате ЧЧ:ММ'
        keyboard = skip_with_default_time_button_keyboard()
    elif field == 'comment' and current:
        keyboard = skip_with_clear_keyboard()
    await state.update_data(field=field)
    await EditEventStates.field_value.set()
    label = EVENT_FIELD_BUTTONS[field]
    await call.message.answer(
        f'{label}: {current or "не заполнено"}\n'
        f'Введите новое значение{hint}.\n'
        f'Кнопка «Пропустить» оставит как есть.',
        reply_markup=keyboard)


async def field_value_input(message: types.Message, state: FSMContext):
    """Новое значение поля: проверить, записать и вернуть карточку."""
    data = await state.get_data()
    field = data['field']
    text = message.text.strip()

    if text == skip_button:
        await show_card(message, state)
        return
    if field == 'comment' and text == clear_comment:
        value = ''
    elif field == 'event_date':
        if not validate_date(text):
            await message.answer('Что-то не так с введенной датой.\n'
                                 'Сообщение должно быть в формате ДД.ММ.ГГ '
                                 '(например 13.04.26).')
            return
        value = convert_date_to_db_format(text)
    elif field == 'event_time':
        if not validate_time(text):
            await message.answer('Что-то не так с введенным временем.\n'
                                 'Сообщение должно быть в формате ЧЧ:ММ '
                                 '(например 12:00 или 23:59).')
            return
        value = convert_time_to_db_format(text)
    else:
        if not validate_string_field(text):
            await message.answer('Что-то не так с введенным текстом.\n'
                                 'Текст не должен содержать символы <> '
                                 'и быть не длиннее 1000 символов.')
            return
        value = text

    await state.update_data({field: value})
    await show_card(message, state)


async def card_save(call: types.CallbackQuery, state: FSMContext):
    """Сохранить отредактированное событие."""
    await call.answer()
    update_event(await state.get_data())
    await state.finish()
    await call.message.answer('Запись отредактирована',
                              reply_markup=main_admin_menu_keyboard())


async def card_cancel(call: types.CallbackQuery, state: FSMContext):
    """Кнопка «Отмена» под сообщением."""
    await call.answer()
    await state.finish()
    await call.message.answer('Операция отменена',
                              reply_markup=main_admin_menu_keyboard())


async def stale_button(call: types.CallbackQuery):
    """Нажата кнопка из старого сообщения."""
    await call.answer('Эта кнопка уже не действует. Начните заново из меню.',
                      show_alert=True)


async def cancel_edit_note(message: types.Message, state: FSMContext):
    """Отмена редактирования события."""
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
    dp.register_message_handler(edit_event_start, text=edit_event_button,
                                state=None)
    dp.register_callback_query_handler(event_chosen, event_cb.filter(),
                                       state=EditEventStates.choose_event)
    dp.register_callback_query_handler(field_chosen, field_cb.filter(),
                                       state=EditEventStates.card)
    dp.register_message_handler(field_value_input,
                                state=EditEventStates.field_value)
    dp.register_callback_query_handler(card_save,
                                       card_cb.filter(action='save'),
                                       state=EditEventStates.card)
    dp.register_callback_query_handler(card_cancel,
                                       card_cb.filter(action='cancel'),
                                       state='*')


def register_stale_button_handler(dp: Dispatcher):
    """Регистрировать последним: ловит кнопки, которые никто не обработал."""
    dp.register_callback_query_handler(stale_button, state='*')
