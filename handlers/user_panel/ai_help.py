import asyncio

from aiogram import F, Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filter.chat_types import ChatTypeFilter
from handlers.ai_function import sent_prompt_and_get_response
from handlers.user_panel.start_functions import send_welcome_message
from keyboard.inline import start_functions_keyboard,get_cancel_keyboard

ai_help_private_router = Router()
ai_help_private_router.message.filter(ChatTypeFilter(['private']))


class AiAssistanceState(StatesGroup):
    WaitingForReview = State()


@ai_help_private_router.callback_query(F.data.startswith("ai_help"))
async def ai_help_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    m = await query.message.edit_caption(
        caption="🀄 Задайте запрос по игре Го, и я постараюсь ответить на ваши вопросы! 🎮\n\n💡"
                " Не стесняйтесь спрашивать о правилах, стратегии или истории игры. Я здесь, чтобы помочь! 😊",
        reply_markup=get_cancel_keyboard()
    )
    await state.update_data(message_id=m.message_id)
    await query.answer("Ждем ваш вопрос! 📝")
    await state.set_state(AiAssistanceState.WaitingForReview)


@ai_help_private_router.callback_query(F.data == "cancel_ai_help")
async def cancel_ai_help(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await query.answer("Ваш запрос отменен. Вы вернулись в главное меню.")
    await query.message.delete()
    await send_welcome_message(query.from_user, query.message)


@ai_help_private_router.message(AiAssistanceState.WaitingForReview)
async def process_help_request(message: types.Message, state: FSMContext,bot: Bot):
    user_info = message.from_user.first_name or ""
    if message.from_user.last_name:
        user_info += f" {message.from_user.last_name}"
    if message.from_user.username:
        user_info += f" (@{message.from_user.username})"

    if message.text:
        # Отправляем сообщение с подтверждением и сохраняем его
        processing_message = await message.answer(f"Запрос принят, {user_info}!\n💭 Ещё чуть-чуть, готовлю ответ...")

        # Генерируем ответ с ИИ
        generated_help = sent_prompt_and_get_response(message.text)
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='↩️ Вернуться', callback_data='return'))
        await bot.edit_message_text(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id,
            text=generated_help,
            reply_markup=keyboard.as_markup()
        )
        user_data = await state.get_data()
        message_id = user_data.get("message_id")

        if message_id:
            # Удаляем сообщение, которое мы редактировали ранее
            await bot.delete_message(message.chat.id, message_id)

        await state.clear()

    else:
        # Если сообщение пустое, удаляем его и отправляем новое сообщение
        await message.delete()
        m = await message.answer("Пожалуйста, задайте свой вопрос.")
        await asyncio.sleep(5)
        await m.delete()

