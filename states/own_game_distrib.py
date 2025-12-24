from aiogram.dispatcher.filters.state import State, StatesGroup


class OwnGameDistribtStates(StatesGroup):
    """Машина состояний распределения игроков Своей Игры."""
    choose_type = State()
    distribute = State()
