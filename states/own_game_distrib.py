from aiogram.dispatcher.filters.state import State, StatesGroup


class OwnGameDistribtStates(StatesGroup):
    """Машина состояний нового события."""
    distribute = State()
