from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_functions_keyboard():
    """Функция для создания клавиатуры."""
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="📖 О нас", callback_data="about_us"))  # Информация о компании
    keyboard.add(InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot"))  # Описание бота

    keyboard.add(InlineKeyboardButton(text="🎓 Мастер-классы", callback_data="workshops"))  # Запись на обучение
    keyboard.add(InlineKeyboardButton(text="🤔 Что такое Го?", callback_data="what_is_go"))  # Описание игры Го
    keyboard.add(
        InlineKeyboardButton(text="🧠 Чем полезна игра Го?", callback_data="benefits_of_go"))  # Преимущества игры
    keyboard.add(InlineKeyboardButton(text="🏆 Что я получу, вступив в клуб Го?", callback_data="what_do_i_get"))

    keyboard.add(InlineKeyboardButton(text="📍 Адреса филиалов", callback_data="branches"))  # Список филиалов
    keyboard.add(InlineKeyboardButton(text="📷 Наш Instagram", url="https://www.instagram.com/sengoku.kg/"))
    keyboard.add(InlineKeyboardButton(text="📞 Связаться с нами", callback_data="contact_us"))  # Контакты

    keyboard.add(InlineKeyboardButton(text="🎮 Игра Го", callback_data="play_go"))  # Мини-игра
    keyboard.add(InlineKeyboardButton(text="🤖 Задать вопрос", callback_data='ai_help'))

    return keyboard.adjust(2, 1, 1, 1, 1, 2, 1).as_markup()


def return_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start"))
    return keyboard.adjust(1, ).as_markup()


def return_from_workshops_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Записаться 🎓", callback_data="register_for_workshop"))
    keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню 🏠", callback_data="start"))
    return keyboard.adjust(1).as_markup()


def return_from_branches_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔎 Посмотреть на 2ГИС 🌍",
                                      url="https://2gis.kg/bishkek/search/sengoku.kg/firm/70000001060100301/74.620524%2C42.827672?m=74.612824%2C42.824463%2F12.04"))
    keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню 🏠", callback_data="start"))
    return keyboard.adjust(1).as_markup()


def contact_us_functions_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="📷 Наш Instagram", url="https://www.instagram.com/sengoku.kg/"))
    keyboard.add(
        InlineKeyboardButton(text="📱 Написать в WhatsApp", url="https://api.whatsapp.com/send/?phone=996509240706"))
    keyboard.add(InlineKeyboardButton(text="🔵 Наш Facebook", url="https://www.facebook.com/sengoku.kg"))
    keyboard.add(InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="start"))

    return keyboard.adjust(1).as_markup()


def get_cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_ai_help"))
    return keyboard.adjust(1).as_markup()
