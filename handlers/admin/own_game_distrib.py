from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from data.services import (
    is_admin,
    make_triple_message,
    make_triples,
    make_triples_snake,
    parse_players,
)
from keyboards.admin.keyboards import (
    cancel_button,
    canсel_keyboard,
    main_admin_menu_keyboard,
    own_game_distrib,
    own_game_order_type,
    own_game_snake_type,
    own_game_type_keyboard,
)
from keyboards.user.keyboards import menu_reply_keyboard
from states.own_game_distrib import OwnGameDistribtStates


async def choose_distribution_type(message: types.Message):
    """Выбрать тип распределения участников на Свояк."""
    telegram_id = message.from_user.id
    admin = is_admin(telegram_id)
    if admin:
        await OwnGameDistribtStates.choose_type.set()
        await message.answer(
            "Выберите тип распределения.\n\n"
            "1. По порядку. Участники делятся на 3 равные части - топ, середина, низ. В первую тройку идёт первое место каждой части. Во вторую - второе и так далее.\n\n"
            "2. Змейкой. Первые N участников (где N - число троек) встают первыми в тройках в прямом порядке, вторые N участников становятся вторыми в обратном порядке."
            "Третьи N участников становятся третьими в прямом порядке.\n\n"
            "Оставшиеся 1-2 участника добавляются четвертыми в нижние тройки в обоих случаях.\n\n"
            "Распределение отработает при количестве участников отборки 6 и более.",
            reply_markup=own_game_type_keyboard(),
        )
    else:
        await message.answer(
            "Ты не админ. Больше так не делай.",
            reply_markup=menu_reply_keyboard(False),
        )


async def begin_distribution(message: types.Message, state: FSMContext):
    """Начало распределения участников на Свояк."""
    async with state.proxy() as data:
        data['type'] = message.text

    await OwnGameDistribtStates.distribute.set()
    await message.answer(
        "Введите результаты отборки одним сообщением.\n"
        "Один участник - одна строка\n"
        "В формате 'Иван Иванов -300'\n\n"
        "Распределение отработает при количестве участников отборки 6 и более.",
        reply_markup=canсel_keyboard(),
    )


async def distribute_players(message: types.Message, state: FSMContext):
    """Распределить игроков."""
    async with state.proxy() as data:
        distr_type = data['type']

    try:
        players = parse_players(message.text)

        if distr_type == own_game_order_type:
            triples = make_triples(players)
        elif distr_type == own_game_snake_type:
            triples = make_triples_snake(players)
        else:
            raise ValueError("Неверный тип распределения")

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
    dp.register_message_handler(
        cancel_distribution,
        text=cancel_button,
        state='*',
    )
    dp.register_message_handler(
        choose_distribution_type,
        text=own_game_distrib,
        state=None,
    )
    dp.register_message_handler(
        begin_distribution,
        text=[own_game_order_type, own_game_snake_type],
        state=OwnGameDistribtStates.choose_type,
    )
    dp.register_message_handler(
        distribute_players,
        state=OwnGameDistribtStates.distribute,
    )
