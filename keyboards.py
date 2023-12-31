from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton(text="Я администратор!"), KeyboardButton(text="Я студент!"))
    return kb


def get_company_kb(company: list) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in company:
        kb.add(KeyboardButton(text=f'{i}'))
    kb.add(KeyboardButton(text="Зарегистрировать новую компанию"))
    return kb


def get_drivers_kb(company: list) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in company:
        kb.add(KeyboardButton(text=f'{i}'))
    return kb


def lk_manager_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Управление мероприятиями"))
    kb.add(KeyboardButton("Мероприятия сегодня"))
    kb.add(KeyboardButton("Обратная связь"))
    return kb

def lk_student_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Список мероприятий"))
    kb.add(KeyboardButton("Мои мероприятия"))
    return kb

def inline_admin_management_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(InlineKeyboardButton("Создать мероприятие", callback_data='create_mero'))
    kb.add(InlineKeyboardButton(text="Посмотреть мероприятия", callback_data="look_mero"))
    kb.add(InlineKeyboardButton(text="Создать конкурс", callback_data='create_compete'))
    kb.add(InlineKeyboardButton(text="Назад в меню", callback_data="back"))
    return kb



