from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from filter.chat_types import ChatTypeFilter, IsAdmin
from keyboard.inline import return_functions_keyboard

play_go_functions_private_router = Router()
play_go_functions_private_router.message.filter(ChatTypeFilter(['private']))


@play_go_functions_private_router.callback_query(F.data == 'play_go')
async def play_go_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_functions_keyboard()

    caption = (
        "Это команда пока что не доступна. Попробуйте позже!"
    )

    await query.message.edit_caption(
        caption=caption,
        reply_markup=keyboard_markup
    )