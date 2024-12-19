from aiogram import F, types, Router, Bot
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from filter.chat_types import ChatTypeFilter
from keyboard.inline import *

start_functions_private_router = Router()
start_functions_private_router.message.filter(ChatTypeFilter(['private']))


async def send_welcome_message(user, target, photo_path='media/images/img.png'):
    """Функция для отправки приветственного сообщения с фото."""
    keyboard_markup = start_functions_keyboard()
    await target.answer_photo(
        photo=types.FSInputFile(photo_path),
        caption=(
            f"Приветствуем, {user.full_name}! 🎉\n\n"
            "Вы попали в официальный Telegram-бот компании Sengokukg 🏯\n"
            "Нажмите на кнопку ниже, чтобы узнать больше о нас, записаться на мастер-классы или "
            "погрузиться в увлекательный мир игры Го! 🎌"
        ),
        reply_markup=keyboard_markup
    )


# Обработчик команды /start
@start_functions_private_router.message(CommandStart())
async def start_cmd(message: types.Message,):
    """Обработчик команды /start"""
    await send_welcome_message(message.from_user, message)


# Обработчик нажатия кнопки "Старт"
@start_functions_private_router.callback_query(F.data == "start")
async def start_main_menu(query: types.CallbackQuery,):
    """Обработчик callback_query для основного меню"""
    await query.message.delete()
    await send_welcome_message(query.from_user, query.message)


@start_functions_private_router.callback_query(F.data == "return")
async def start_menu(query: types.CallbackQuery,):
    """Обработчик callback_query для основного меню"""
    await send_welcome_message(query.from_user, query.message)


@start_functions_private_router.callback_query(F.data == 'about_us')
async def about_us_command_callback_query(query: types.CallbackQuery) -> None:
    await query.message.delete()
    keyboard_markup = return_functions_keyboard()
    await query.message.answer_photo(
        photo=types.FSInputFile('media/images/img_1.png'),
        caption=(
            "Мы — сеть Го-клубов Кыргызстана <b>Sengoku</b>, объединяющая людей, увлечённых древней настольной игрой Го. 🎯\n\n"
            "<b>✨ Наша миссия:</b> популяризировать игру Го, помогая каждому развивать стратегическое мышление и находить гармонию.\n\n"
            "Что мы предлагаем:\n"
            "🎓 <b>Обучение игре Го</b> для новичков и продвинутых игроков.\n"
            "🧠 <b>Мастер-классы</b> и регулярные занятия для всех возрастов.\n"
            "🏆 Организацию турниров и участие в международных мероприятиях.\n"
            "🤝 Уютное сообщество единомышленников, где можно найти друзей и наставников.\n\n"
            "Присоединяйтесь к нам и откройте для себя мир Го — игры, которая обучает терпению и стратегическому мышлению! 🌟"
        ),
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'about_bot')
async def about_bot_command_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_functions_keyboard()
    await query.message.edit_caption(
        caption="💬 Привет! Этот бот был создан, чтобы сделать взаимодействие с нашей компанией еще проще! 👌\n\n"
                "👻 Узнай все о наших мастер-классах, 📃 адресах филиалов и многом другом.\n\n"
                "🎁 С помощью этого бота ты сможешь записаться на события, получить важную информацию и даже сыграть в увлекательную игру Го! 💡\n\n"
                "Нажми на кнопку ниже, чтобы вернуться в главное меню!",
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'workshops')
async def workshops_command_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_from_workshops_functions_keyboard()
    await query.message.edit_caption(
        caption=(
            "🎓 <b>Мастер-классы по игре Го</b>\n\n"
            "Погрузитесь в мир Го вместе с нашими профессиональными инструкторами! На мастер-классах вы узнаете:\n"
            "🔹 Основные правила и стратегии игры Го.\n"
            "🔹 Секреты тактического и стратегического мышления.\n"
            "🔹 Приёмы, которые помогут вам побеждать в турнирах.\n\n"
            "🌟 Наши мастер-классы подойдут как для новичков, так и для опытных игроков. Присоединяйтесь, чтобы улучшить свои навыки и открыть для себя новые грани этой удивительной игры!"
        ),
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == "register_for_workshop")
async def register_for_workshop_callback_query(query: types.CallbackQuery, bot: Bot):
    """Обработчик callback_query для записи на мастер-класс"""
    keyboard_markup = return_functions_keyboard()
    text = "Ваша заявка отправлена нашему менеджеру, он свяжется с вами в ближайшее время. 💬"
    await query.message.edit_caption(
        caption=text,
        reply_markup=keyboard_markup
    )
    await query.answer(text=text)
    for manager_id in bot.my_admins_list:  # Убедитесь, что у вас есть список менеджеров
        user_info = f"📝 {query.from_user.first_name}"

        # Добавляем фамилию, если она есть
        if query.from_user.last_name:
            user_info += f" {query.from_user.last_name}"

        # Добавляем username, если он есть
        if query.from_user.username:
            user_info += f" (@{query.from_user.username})"

        # Отправляем сообщение менеджерам
        await bot.send_message(
            manager_id,text=
            f"💼 <b>Новая заявка на мастер-класс</b>:\n\n"
            f"👤 <b>Информация о пользователе:</b>\n"
            f"📛 <b>Имя:</b> {user_info}\n"
            f"📲 <b>Контакт пользователя:</b> @{query.from_user.username or 'Не указан'}\n\n"
            f"🔑 <b>Ваши действия:</b>\n"
            f"1. Напишите пользователю для подтверждения заявки.\n")


@start_functions_private_router.callback_query(F.data == 'what_is_go')
async def what_is_go_callback_query(query: types.CallbackQuery) -> None:
    await query.message.delete()
    keyboard_markup = return_functions_keyboard()

    caption = (
        "⚫️⚪️ <b>Что такое Го?</b> 🤔 Пойдемте разбираться! 🌟\n\n"
        "Го — одна из самых популярных настольных стратегических игр Японии, Кореи и Китая. "
        "Её правила просты, но игра может стать весьма сложной и увлекательной! 😲\n\n"
        "Цель игры — огородить на доске камнями своего цвета большую территорию, чем у противника. "
        "Го превосходит шахматы своей простотой, но не уступает в богатстве стратегий и тактик. ♟️\n\n"

        "<b>Факты о Го:</b>\n"
        "👑 В Го играет более 50 миллионов людей по всему миру.\n"
        "💵 Профессионалы зарабатывают до 1 млн долларов в год.\n"
        "🔢 В Го существует более 16 миллиардов возможных позиций, в отличие от шахмат, где после четвертого хода их всего около 100 тыс.\n\n"

        "<b>Система рангов в Го:</b>\n"
        "🥇 Ученические ранги варьируются от 30 кю (начальный) до 1 кю (высший).\n"
        "🏅 Ранги мастеров — от 1 дана до 9 дана (высший).\n"
        "🎓 Пройдя наш мастер-класс, вы получите ранг 25 кю — это значит, что вы уже знаете правила и пару раз сыграли! 💪\n\n"
        "Погружайтесь в увлекательный мир Го с нами! 🚀"
    )

    await query.message.answer_photo(
        photo=types.FSInputFile('media/images/img_3.png'),
        caption=caption,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'benefits_of_go')
async def benefits_of_go_callback_query(query: types.CallbackQuery) -> None:
    await query.message.delete()
    keyboard_markup = return_functions_keyboard()

    caption = (
        "<b>⚫️⚪️ Чем полезна игра Го?</b>\n\n"
        "Игра Го развивает важные навыки и способности, полезные как в игре, так и в жизни:\n\n"

        "<b>🔶 Универсальность стратегий</b> и параллели с другими сферами;\n"
        "<b>🔶 Развитие комбинаторики и пространственного мышления</b>;\n"
        "<b>🔶 Комплексное развитие мозга</b> — активизация 16 отделов мозга;\n"
        "<b>🔶 Глубокая философия и культура</b> игры, её принципы применимы в жизни и бизнесе;\n"
        "<b>🔶 Принципы Го в бизнесе</b> — стратегия и многофакторный анализ.\n\n"

        "<i>☝️ Го — это инструмент для развития и осознания, который помогает мыслить на более глубоком уровне.</i>"
    )

    await query.message.answer_photo(
        photo=types.FSInputFile('media/images/img_2.png'),
        caption=caption,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'what_do_i_get')
async def what_do_i_get_callback_query(query: types.CallbackQuery) -> None:
    await query.message.delete()
    keyboard_markup = return_functions_keyboard()

    caption = (
        "<b>Предлагаем вам погрузиться в захватывающий мир Го!</b>😉\n\n"
        "Что вас ждёт в нашем Го-клубе?👇😍\n\n"
        "<b>🔹 Курсы Го:</b> стратегии, аналитика, разборы, задачи;\n"
        "<b>🔹 Игровые дни</b> по выходным;\n"
        "<b>🔹 Фильмы и аниме</b> по Го;\n"
        "<b>🔹 Крутое комьюнити</b> и нетворкинг;\n"
        "<b>🔹 Турниры с призовыми</b>;\n"
        "<b>🔹 Официальный европейский ранг</b>;\n"
        "<b>🔹 Возможность стать тренером</b>;\n"
        "<b>🔹 Профессиональная спортивная карьера</b>.\n\n"
        "<i>Наш Го-клуб ждёт вас!😉</i>"
    )

    await query.message.answer_photo(
        photo=types.FSInputFile('media/images/img_4.png'),
        caption=caption,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'branches')
async def branches_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_from_branches_functions_keyboard()
    caption = (
        "<b>⏰ Время работы:</b> Пн-Пт 09:00-20:00\n\n"
        "<b>📍 Наш филиал находится по адресу:</b>\n"
        "Адрес: Абдрахманова 101, вход со стороны \"Бонсай\"\n"
        "График: 14:00-19:00 (будни), 12:00-18:00 (выходные)"
    )
    await query.message.edit_caption(
        caption=caption,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'contact_us')
async def contact_us_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = contact_us_functions_keyboard()

    caption = (
        "Если у вас есть вопросы или предложения, мы всегда рады помочь! 😄\n\n"
        "Вы можете связаться с нами через следующие каналы:\n\n"
        "📷 Наш Instagram\n"
        "📱 Написать в WhatsApp\n"
        "🔵 Наш Facebook\n\n"
        "Если нужно, вернитесь в главное меню с помощью кнопки ниже. 🏠"
    )

    await query.message.edit_caption(
        caption=caption,
        reply_markup=keyboard_markup
    )

