from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from data.services import is_admin, make_triple_message, make_triples, parse_players
from keyboards.admin.keyboards import (
    cancel_button,
    canсel_keyboard,
    main_admin_menu_keyboard,
    own_game_distrib,
)
from keyboards.user.keyboards import menu_reply_keyboard
from states.own_game_distrib import OwnGameDistribtStates


async def begin_distribution(message: types.Message):
    """Начало распределения участников на Свояк."""
    telegram_id = message.from_user.id
    admin = is_admin(telegram_id)
    if admin:
        await OwnGameDistribtStates.distribute.set()
        await message.answer(
            "Введите результаты отборки одним сообщением.\n"
            "Один участник - одна строка\n"
            "В формате 'Иван Иванов -300'\n\n"
            "Распределение отработает при количестве участников отборки 6 и более.",
            reply_markup=canсel_keyboard(),
        )
    else:
        await message.answer(
            "Ты не админ. Больше так не делай.",
            reply_markup=menu_reply_keyboard(False),
        )


async def distribute_players(message: types.Message, state: FSMContext):
    """Распределить игроков."""
    try:
        players = parse_players(message.text)
        triples = make_triples(players)
        answer = make_triple_message(triples)
        await message.answer(
            answer,
            reply_markup=main_admin_menu_keyboard(),
        )
    except ValueError as e:
        await message.answer(
            f"{e}\n"
            "Начните заново.",
            reply_markup=main_admin_menu_keyboard(),
        )
    except Exception as e:
        await message.answer(
            f"Что-то пошло не так: {e}\n"
            "Начните заново.",
            reply_markup=main_admin_menu_keyboard(),
        )
    finally:
        await state.finish()


async def cancel_distribution(message: types.Message, state: FSMContext):
    """Отмена распределения."""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Операция отменена',
                             reply_markup=main_admin_menu_keyboard())
    else:
        await message.answer('Так ведь нечего отменять',
                             reply_markup=menu_reply_keyboard(True))


def register_own_game_distribution_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_distribution, text=cancel_button, state='*')
    dp.register_message_handler(begin_distribution, text=own_game_distrib, state=None)
    dp.register_message_handler(distribute_players, state=OwnGameDistribtStates.distribute)
