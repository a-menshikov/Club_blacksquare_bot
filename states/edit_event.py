from aiogram.dispatcher.filters.state import State, StatesGroup


class EditEventStates(StatesGroup):
    """Машина состояний редактирования события."""
    event_id = State()
    name = State()
    event_date = State()
    event_time = State()
    complexity = State()
    payment = State()
    comment = State()
    approve = State()
