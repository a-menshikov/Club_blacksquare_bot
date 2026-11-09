from aiogram.dispatcher.filters.state import State, StatesGroup


class EditEventStates(StatesGroup):
    """Машина состояний редактирования события."""
    choose_event = State()
    card = State()
    field_value = State()
