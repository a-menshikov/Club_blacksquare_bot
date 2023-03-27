from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteEventStates(StatesGroup):
    """Машина состояний удаления события."""
    event_id = State()
    approve = State()
