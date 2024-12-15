from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from filter.chat_types import ChatTypeFilter, IsAdmin
from keyboard.inline import *

play_go_functions_private_router = Router()
play_go_functions_private_router.message.filter(ChatTypeFilter(['private']))


@play_go_functions_private_router.callback_query(F.data == 'play_go')
async def play_go_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = start_game_functions_keyboard()

    caption = (
        "<b>🎮 Добро пожаловать в игру!</b>\n\n"
        "Для начала выберите действие, которое хотите выполнить.\n"
        "Вы можете ознакомиться с правилами игры или начать играть прямо сейчас!"
    )

    await query.message.edit_caption(
        caption=caption,
        reply_markup=keyboard_markup
    )


@play_go_functions_private_router.callback_query(F.data == 'game_rules')
async def game_rules_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_game_functions_keyboard()

    caption = (
        "<b>🎮 Правила игры в Го</b>\n\n"
        "<b>1️⃣ Инвентарь:</b> Игра на доске 19x19 линий с черными и белыми камнями.\n"
        "<b>2️⃣ Цель игры:</b> Окружить камни противника и захватить их.\n"
        "<b>3️⃣ Правила хода:</b> Игроки по очереди ставят камни на доску.\n"
        "<b>4️⃣ Захват камней:</b> Камни, не имеющие точек свободы, захватываются и снимаются с доски.\n"
        "<b>5️⃣ Коми:</b> Белому игроку добавляется бонус за второй ход.\n"
        "<b>6️⃣ Фора:</b> Слабейший игрок может получить форовые камни.\n"
        "<b>7️⃣ Конец игры:</b> Игра заканчивается, когда оба игрока пасуют.\n"
        "<b>8️⃣ Правила Го:</b> Разные варианты правил могут существовать в зависимости от региона.\n"
    )

    await query.message.edit_caption(
        caption=caption,
        reply_markup=keyboard_markup
    )

@play_go_functions_private_router.callback_query(F.data == 'start_game')
async def start_game_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_game_functions_keyboard()

    caption = (
        "Это команда пока что не доступна. Попробуйте позже!"
    )

    await query.message.edit_caption(
        caption=caption,
        reply_markup=keyboard_markup
    )
