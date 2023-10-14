import config
from config import TOKEN_API
from aiogram import Dispatcher, Bot, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, InputFile, WebAppInfo
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import get_start_kb, get_company_kb, lk_manager_kb, inline_admin_management_kb, get_drivers_kb, \
    inline_company_management_kb, inline_vehicle_control_kb
from aiogram.dispatcher import FSMContext


storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

list_vehicle = ['мерс', 'бэха']

dict_managers = {'firstname': ['1'],
                 "lastname": ["1"],
                 "company_id": [1]}
list_drivers = ["Нечаев"]
dict_drivers = {'firstname': ['Олег', "Анрей", "Игорь", "Жанна"],
                "lastname": ["Нечаев", "Богомольцев", "Сапожников", "Нечинская"],
                'telegram_id': [1, 2, 3, 4],
                "company_id": [1, 2, 3, 4],
                "state": ["В пути", "Простаивает", "Прибыл на загрузку", "Прибыл на выгрузку"]}

dict_login_manager = {}

dict_company = {'name': ["Новатэк", "ПКЛПО", "Грузы из Лиссабона", "Энергия"],
                "company_id": [1, 2, 3, 4]}
dict_vehicle = {'name': ['мерс', 'бэха'],
                'state': ['Занята', 'не занята'],
                'mark': ['12', '133'],
                "model": ['11', '22']}


class ProfileMenuGroup(StatesGroup):
    menu_state = State()
    menu_back = State()


class ProfileCreateMeroStatesGroup(StatesGroup):
    admin = State()
    add_mero_name = State()
    add_mero_databegin = State()
    add_mero_dataEnd = State()
    add_mero_deadline = State()
    add_mero_place = State()
    add_mero_sitelink = State()


class ProfileCreateCompetStatesGroup(StatesGroup):
    admin = State()
    add_compet_name = State()
    add_compet_databegin = State()
    add_compet_dataEnd = State()
    add_compet_deadline = State()
    add_compet_place = State()
    add_compet_sitelink = State()
    add_compet_value = State()


class ProfileManagerLoginStatesGroup(StatesGroup):
    manager_login_name = State()
    manager_login_surname = State()
    manager_login_patronymic = State()
    manager_login_id = State()


class ProfileManagerStatesGroup(StatesGroup):
    manager_reg_name = State()
    manager_reg_surname = State()
    manager_reg_patronymic = State()
    manager_reg_id = State()


class ProfileMeroChoice(StatesGroup):
    drones_competition_outside_choice = State()
    soft_skills_competition_outside_choice = State()
    it_competition_outside_choice = State()
    radio_electronics_competition_outside_choice = State()
    social_competition_outside_choice = State()
    entertainment_competition_outside_choice = State()
    no_category_competition_outside_choice = State()
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    drones_event_outside_choice = State()
    soft_skills_event_outside_choice = State()
    it_event_outside_choice = State()
    radio_electronics_event_outside_choice = State()
    social_event_outside_choice = State()
    entertainment_event_outside_choice = State()
    no_category_event_outside_choice = State()
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    drones_competition_inside_choice = State()
    soft_skills_competition_inside_choice = State()
    it_competition_inside_choice = State()
    radio_electronics_competition_inside_choice = State()
    social_competition_inside_choice = State()
    entertainment_competition_inside_choice = State()
    no_category_competition_inside_choice = State()
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    drones_event_inside_choice = State()
    soft_skills_event_inside_choice = State()
    it_event_inside_choice = State()
    radio_electronics_event_inside_choice = State()
    social_event_inside_choice = State()
    entertainment_event_inside_choice = State()
    no_category_event_inside_choice = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в нашего бота! Пожалуйста сообщи кто ты :)',
                           reply_markup=get_start_kb())
    await message.delete()


@dp.message_handler(lambda message: message.text in ['Я администратор!', 'Я студент!'])
async def driver_or_manager(message: types.Message) -> None:
    if message.text == "Я администратор!":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Ты уже зарегистрирован?.",
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                                   KeyboardButton('Да'), KeyboardButton('Нет')))


@dp.message_handler(lambda message: message.text.lower() in ['да', 'нет'])
async def reg_yes_or_not(message: types.Message) -> None:
    if message.text.lower() == 'да':
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введи своё имя")
        await ProfileManagerLoginStatesGroup.manager_login_name.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Давай зарегистрируемся, введи своё имя")
        await ProfileManagerStatesGroup.manager_reg_name.set()


@dp.message_handler(lambda message: message.text == 'Повторить ввод данных')
async def repetitive_login(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введи своё имя')
    await ProfileManagerLoginStatesGroup.manager_login_name.set()


@dp.message_handler(lambda message: message.text == 'Зарегистрироваться')
async def repetitive_reg(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введи своё имя')
    await ProfileManagerStatesGroup.manager_reg_name.set()


@dp.message_handler(state=ProfileManagerStatesGroup.manager_reg_name)
async def state_manager_reg_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text

    await bot.send_message(chat_id=message.from_user.id, text='Теперь введи свою фамилию')
    await ProfileManagerStatesGroup.manager_reg_surname.set()


@dp.message_handler(lambda message: message.text == 'Обратная связь', state=ProfileMenuGroup.menu_state)
async def feedback(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"""CEO проекта - @macgoodmonsta \nРазработчик - @qecal \nРазработчик - @Qw_wi \nРазработчик - @smnv_vs \nРазработчик - @ml_nastya""",
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                               KeyboardButton("Google Forms", web_app=WebAppInfo(
                                   url='https://docs.google.com/forms/d/16nMg62qwL3OxZawuP54ZWljUUTwJ8Pq8L23AS8SxzGc/edit')),
                               KeyboardButton("Меню")
                           ))
    await ProfileMenuGroup.menu_back.set()


@dp.message_handler(state=ProfileManagerStatesGroup.manager_reg_surname)
async def state_manager_req_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text

    await bot.send_message(chat_id=message.from_user.id,
                           text="Введи отчество")
    await ProfileManagerStatesGroup.manager_reg_patronymic.set()


@dp.message_handler(state=ProfileManagerStatesGroup.manager_reg_patronymic)
async def state_manager_req_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['patronymic'] = message.text

    await bot.send_message(chat_id=message.from_user.id,
                           text="Введи идентификационный номер")
    await ProfileManagerStatesGroup.manager_reg_id.set()


@dp.message_handler(state=ProfileManagerStatesGroup.manager_reg_id)
async def state_manager_req_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text

    await bot.send_message(chat_id=message.from_user.id,
                           text="Ты успешно зарегистрировался")
    await bot.send_message(chat_id=message.from_user.id,
                           text="Добро пожаловать в личный кабинет!",
                           reply_markup=lk_manager_kb())
    await ProfileMenuGroup.menu_state.set()


@dp.message_handler(state=ProfileMenuGroup.menu_state)
async def driver_management(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text == "Управление мероприятиями":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                               reply_markup=inline_admin_management_kb())
        await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'coordination_mero',
                           state=ProfileCreateMeroStatesGroup.admin)
async def coordination_mero(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(
        text="Используя кнопки под этим сообщением можно управлять мероприятиями",
        reply_markup=inline_admin_management_kb())
    await state.finish()
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "back",
                           state=ProfileCreateMeroStatesGroup.admin)
async def back(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer(text="Добро пожаловать в личный кабинет!",
                                  reply_markup=lk_manager_kb())
    await ProfileMenuGroup.menu_state.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'create_mero',
                           state=ProfileCreateMeroStatesGroup.admin)
async def create_mero(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Переходим к добавлению мероприятия, напишите его название")
    await ProfileCreateMeroStatesGroup.add_mero_name.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'create_compete',
                           state=ProfileCreateMeroStatesGroup.admin)
async def create_compet(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Переходим к добавлению конкурса, напишите его название")
    await ProfileCreateCompetStatesGroup.add_compet_name.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'look_mero',
                           state=ProfileCreateMeroStatesGroup.admin)
async def look_mero(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Выберите какое мероприятие нужно",
                                  reply_markup=InlineKeyboardMarkup().add(
                                      InlineKeyboardButton(text="Внутри ГУАП", callback_data="inside_suai"),
                                      InlineKeyboardButton(text="Вне ГУАП", callback_data="outside_suai")))


@dp.callback_query_handler(lambda callback_query: callback_query.data in ['inside_suai', "outside_suai"],
                           state=ProfileCreateMeroStatesGroup.admin)
async def look_mero_2(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "outside_suai":
        await callback.message.edit_text(text="Фильтр мероприятий",
                                         reply_markup=InlineKeyboardMarkup().add(
                                             InlineKeyboardButton(text="Мероприятие", callback_data="event_outside"),
                                             InlineKeyboardButton(text="Соревнование",
                                                                  callback_data="competition_outside")))
    else:
        await callback.message.edit_text(text="Фильтр мероприятий",
                                         reply_markup=InlineKeyboardMarkup().add(
                                             InlineKeyboardButton(text="Мероприятие", callback_data="event_inside"),
                                             InlineKeyboardButton(text="Соревнование",
                                                                  callback_data="competition_inside")
                                         ))


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'competition_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def forum_outside(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Категории мероприятий",
                                     reply_markup=InlineKeyboardMarkup().add(
                                         InlineKeyboardButton(text="Беспилотники",
                                                              callback_data="drones_competition_outside"),
                                         InlineKeyboardButton(text="Soft Skills",
                                                              callback_data="soft_skills_competition_outside"),
                                         InlineKeyboardButton(text="IT/Программирование",
                                                              callback_data="it_competition_outside"),
                                         InlineKeyboardButton(text="Радиоэлектроника",
                                                              callback_data="radio_electronics_competition_outside"),
                                         InlineKeyboardButton(text="Социальные",
                                                              callback_data="social_competition_outside"),
                                         InlineKeyboardButton(text="Развлекательные",
                                                              callback_data="entertainment_competition_outside"),
                                         InlineKeyboardButton(text="Без категориии",
                                                              callback_data="no_category_competition_outside")
                                     ))


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'event_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def forum_outside(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Категории мероприятий",
                                     reply_markup=InlineKeyboardMarkup().add(
                                         InlineKeyboardButton(text="Беспилотники",
                                                              callback_data="drones_event_outside"),
                                         InlineKeyboardButton(text="Soft Skills",
                                                              callback_data="soft_skills_event_outside"),
                                         InlineKeyboardButton(text="IT/Программирование",
                                                              callback_data="it_event_outside"),
                                         InlineKeyboardButton(text="Радиоэлектроника",
                                                              callback_data="radio_electronics_event_outside"),
                                         InlineKeyboardButton(text="Социальные",
                                                              callback_data="social_event_outside"),
                                         InlineKeyboardButton(text="Развлекательные",
                                                              callback_data="entertainment_event_outside"),
                                         InlineKeyboardButton(text="Без категориии",
                                                              callback_data="no_category_event_outside")
                                     ))


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'competition_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def forum_outside(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Категории мероприятий",
                                     reply_markup=InlineKeyboardMarkup().add(
                                         InlineKeyboardButton(text="Беспилотники",
                                                              callback_data="drones_competition_inside"),
                                         InlineKeyboardButton(text="Soft Skills",
                                                              callback_data="soft_skills_competition_inside"),
                                         InlineKeyboardButton(text="IT/Программирование",
                                                              callback_data="it_competition_inside"),
                                         InlineKeyboardButton(text="Радиоэлектроника",
                                                              callback_data="radio_electronics_competition_inside"),
                                         InlineKeyboardButton(text="Социальные",
                                                              callback_data="social_competition_inside"),
                                         InlineKeyboardButton(text="Развлекательные",
                                                              callback_data="entertainment_competition_inside"),
                                         InlineKeyboardButton(text="Без категориии",
                                                              callback_data="no_category_competition_inside")
                                     ))


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'event_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def conference_outside(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Категории мероприятий",
                                     reply_markup=InlineKeyboardMarkup().add(
                                         InlineKeyboardButton(text="Беспилотники",
                                                              callback_data="drones_event_inside"),
                                         InlineKeyboardButton(text="Soft Skills",
                                                              callback_data="soft_skills_event_inside"),
                                         InlineKeyboardButton(text="IT/Программирование",
                                                              callback_data="it_event_inside"),
                                         InlineKeyboardButton(text="Радиоэлектроника",
                                                              callback_data="radio_electronics_event_inside"),
                                         InlineKeyboardButton(text="Социальные",
                                                              callback_data="social_event_inside"),
                                         InlineKeyboardButton(text="Развлекательные",
                                                              callback_data="entertainment_event_inside"),
                                         InlineKeyboardButton(text="Без категориии",
                                                              callback_data="no_category_event_inside")
                                     ))


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'drones_event_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.drones_event_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'soft_skills_event_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.soft_skills_event_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'it_event_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.it_event_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'radio_electronics_event_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.radio_electronics_event_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'social_event_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.social_event_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'entertainment_event_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.entertainment_event_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'no_category_event_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.no_category_event_inside_choice.set()


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'drones_competition_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.drones_competition_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'soft_skills_competition_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.soft_skills_competition_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'it_competition_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.it_competition_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'radio_electronics_competition_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.radio_electronics_competition_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'social_competition_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await (ProfileMeroChoice.social_competition_inside_choice.set())


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'entertainment_competition_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.entertainment_competition_inside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'no_category_competition_inside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.no_category_competition_inside_choice.set()


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'drones_competition_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.drones_competition_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'soft_skills_competition_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.soft_skills_competition_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'it_competition_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.it_competition_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'radio_electronics_competition_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await (ProfileMeroChoice.radio_electronics_competition_outside_choice.set())


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'social_competition_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.social_competition_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'entertainment_competition_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.entertainment_competition_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'no_category_competition_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.no_category_competition_outside_choice.set()


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'drones_event_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.drones_event_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'soft_skills_event_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.soft_skills_event_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'it_event_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.it_event_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'radio_electronics_event_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.radio_electronics_event_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'social_event_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.social_event_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'entertainment_event_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.entertainment_event_outside_choice.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'no_category_event_outside',
                           state=ProfileCreateMeroStatesGroup.admin)
async def drones_forum_outside(callback: types.CallbackQuery, state: FSMContext):
    data = ['qweq', 'qweew']  # список найденных мероприятий из бд
    ttext = f'Найденные мероприятия:\n'
    for i in range(len(data)):
        ttext += f'{i}) {data[i]}'
    await callback.message.answer(text="Выберите нужное мероприятия",
                                  reply_markup=get_drivers_kb(data))
    await ProfileMeroChoice.no_category_event_outside_choice.set()


@dp.message_handler(state=ProfileMeroChoice.drones_competition_outside_choice)
async def add_bd_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="drones_competition_outside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'drones_competition_outside_choice_notify_about_event',
    state=ProfileMeroChoice.drones_competition_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.soft_skills_competition_outside_choice)
async def add_bd_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="soft_skills_competition_outside_choice_notify_about_event")))

@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'soft_skills_competition_outside_choice_notify_about_event',
    state=ProfileMeroChoice.soft_skills_competition_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()
@dp.message_handler(state=ProfileMeroChoice.it_competition_outside_choice)
async def add_bd_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="it_competition_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'it_competition_outside_choice_notify_about_event',
    state=ProfileMeroChoice.it_competition_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.radio_electronics_competition_outside_choice)
async def add_bd_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="radio_electronics_competition_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'radio_electronics_competition_outside_choice_notify_about_event',
    state=ProfileMeroChoice.radio_electronics_competition_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.social_competition_outside_choice)
async def add_bd_5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="social_competition_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'social_competition_outside_choice_notify_about_event',
    state=ProfileMeroChoice.social_competition_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.entertainment_competition_outside_choice)
async def add_bd_6(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="entertainment_competition_outside_choice_notify_about_event")))

@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'entertainment_competition_outside_choice_notify_about_event',
    state=ProfileMeroChoice.entertainment_competition_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()
@dp.message_handler(state=ProfileMeroChoice.no_category_competition_outside_choice)
async def add_bd_7(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="no_category_competition_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'no_category_competition_outside_choice_notify_about_event',
    state=ProfileMeroChoice.no_category_competition_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.drones_event_outside_choice)
async def add_bd_8(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="drones_event_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'drones_event_outside_choice_notify_about_event',
    state=ProfileMeroChoice.drones_event_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.soft_skills_event_outside_choice)
async def add_bd_9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="soft_skills_event_outside_choice_notify_about_event")))

@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'soft_skills_event_outside_choice_notify_about_event',
    state=ProfileMeroChoice.soft_skills_event_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()
@dp.message_handler(state=ProfileMeroChoice.it_event_outside_choice)
async def add_bd_10(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="it_event_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'it_event_outside_choice_notify_about_event',
    state=ProfileMeroChoice.it_event_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.radio_electronics_event_outside_choice)
async def add_bd_11(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="radio_electronics_event_outside_choice_notify_about_event")))

@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'radio_electronics_event_outside_choice_notify_about_event',
    state=ProfileMeroChoice.radio_electronics_event_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()
@dp.message_handler(state=ProfileMeroChoice.social_event_outside_choice)
async def add_bd_12(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="social_event_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'social_event_outside_choice_notify_about_event',
    state=ProfileMeroChoice.social_event_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.entertainment_event_outside_choice)
async def add_bd_13(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="entertainment_event_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'entertainment_event_outside_choice_notify_about_event',
    state=ProfileMeroChoice.entertainment_event_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.no_category_event_outside_choice)
async def add_bd_14(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Уведомить о мероприятии",
                                                                                        callback_data="no_category_event_outside_choice_notify_about_event")))
@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'no_category_event_outside_choice_notify_about_event',
    state=ProfileMeroChoice.no_category_event_outside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()

@dp.message_handler(state=ProfileMeroChoice.drones_competition_inside_choice)
async def add_bd_15(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='drones_competition_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="drones_competition_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'drones_competition_inside_choice_cancel_event',
    state=ProfileMeroChoice.drones_competition_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'drones_competition_inside_choice_notify_about_event',
    state=ProfileMeroChoice.drones_competition_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.soft_skills_competition_inside_choice)
async def add_bd_16(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='soft_skills_competition_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="soft_skills_competition_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'soft_skills_competition_inside_choice_cancel_event',
    state=ProfileMeroChoice.soft_skills_competition_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'soft_skills_competition_inside_choice_notify_about_event',
    state=ProfileMeroChoice.soft_skills_competition_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.it_competition_inside_choice)
async def add_bd_17(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='it_competition_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="it_competition_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'it_competition_inside_choice_cancel_event',
    state=ProfileMeroChoice.it_competition_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...  # удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'it_competition_inside_choice_notify_about_event',
    state=ProfileMeroChoice.it_competition_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.radio_electronics_competition_inside_choice)
async def add_bd_18(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='radio_electronics_competition_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="radio_electronics_competition_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'radio_electronics_competition_inside_choice_cancel_event',
    state=ProfileMeroChoice.radio_electronics_competition_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'radio_electronics_competition_inside_choice_notify_about_event',
    state=ProfileMeroChoice.radio_electronics_competition_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.social_competition_inside_choice)
async def add_bd_19(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='social_competition_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="social_competition_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'social_competition_inside_choice_cancel_event',
    state=ProfileMeroChoice.social_competition_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'social_competition_inside_choice_notify_about_event',
    state=ProfileMeroChoice.social_competition_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.entertainment_competition_inside_choice)
async def add_bd_20(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='entertainment_competition_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="entertainment_competition_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'entertainment_competition_inside_choice_cancel_event',
    state=ProfileMeroChoice.entertainment_competition_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ... # удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'entertainment_competition_inside_choice_notify_about_event',
    state=ProfileMeroChoice.entertainment_competition_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.no_category_competition_inside_choice)
async def add_bd_21(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='no_category_competition_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="no_category_competition_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'no_category_competition_inside_choice_cancel_event',
    state=ProfileMeroChoice.no_category_competition_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'no_category_competition_inside_choice_notify_about_event',
    state=ProfileMeroChoice.no_category_competition_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.drones_event_inside_choice)
async def add_bd_22(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='drones_event_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="drones_event_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'drones_event_inside_choice_cancel_event',
    state=ProfileMeroChoice.drones_event_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'drones_event_inside_choice_notify_about_event',
    state=ProfileMeroChoice.drones_event_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.soft_skills_event_inside_choice)
async def add_bd_23(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='soft_skills_event_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="soft_skills_event_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'soft_skills_event_inside_choice_cancel_event',
    state=ProfileMeroChoice.soft_skills_event_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'soft_skills_event_inside_choice_notify_about_event',
    state=ProfileMeroChoice.soft_skills_event_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.it_event_inside_choice)
async def add_bd_24(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='it_event_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="it_event_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'it_event_inside_choice_cancel_event',
    state=ProfileMeroChoice.it_event_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'it_event_inside_choice_notify_about_event',
    state=ProfileMeroChoice.it_event_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.radio_electronics_event_inside_choice)
async def add_bd_25(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='radio_electronics_event_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="radio_electronics_event_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'radio_electronics_event_inside_choice_cancel_event',
    state=ProfileMeroChoice.radio_electronics_event_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'radio_electronics_event_inside_choice_notify_about_event',
    state=ProfileMeroChoice.radio_electronics_event_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.social_event_inside_choice)
async def add_bd_26(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='social_event_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="social_event_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'social_event_inside_choice_cancel_event',
    state=ProfileMeroChoice.social_event_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...  # удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'social_event_inside_choice_notify_about_event',
    state=ProfileMeroChoice.social_event_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.entertainment_event_inside_choice)
async def add_bd_27(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='entertainment_event_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="entertainment_event_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'entertainment_event_inside_choice_cancel_event',
    state=ProfileMeroChoice.entertainment_event_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'entertainment_event_inside_choice_notify_about_event',
    state=ProfileMeroChoice.entertainment_event_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileMeroChoice.no_category_event_inside_choice)
async def add_bd_28(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вы выбрали: {message.text}",
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("Отменить меропритие",
                                                    callback_data='no_category_event_inside_choice_cancel_event'),
                               InlineKeyboardButton("Уведомить о мероприятии",
                                                    callback_data="no_category_event_inside_choice_notify_about_event")))


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'no_category_event_inside_choice_cancel_event',
    state=ProfileMeroChoice.no_category_event_inside_choice)
async def add_bd_14_cancel_event(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # удаляем меро
        ...# удаляем меро
    await callback.message.answer(text="Вы успешно отменили мероприятие")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'no_category_event_inside_choice_notify_about_event',
    state=ProfileMeroChoice.no_category_event_inside_choice)
async def add_bd_14_notify_about_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Пожалуйста подождите")
    async with state.proxy() as data:
        mero = data['event']  # название мероприятия
        list_id = ['6479804715']  # тут должны быть id студентов по мероприятию
        for i in range(len(list_id)):
            await bot.send_message(chat_id=list_id[i],
                                   text=f'Не забудьте посетить это мероприятие: {data["event"]}')
    await callback.message.answer(
        text="Вы отправили уведомление всем студентам которые зарегистрировались на мероприятие.")
    await callback.message.answer(text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                                  reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'create_compete',
                           state=ProfileCreateMeroStatesGroup.admin)
async def create_compet(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Переходим к добавлению конкурса, напишите его название")
    await ProfileCreateCompetStatesGroup.add_compet_name.set()


@dp.message_handler(state=ProfileCreateCompetStatesGroup.add_compet_name)
async def add_name_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["title"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введите дату начала в формате xx.xx.xxxx ')
    await ProfileCreateCompetStatesGroup.add_compet_databegin.set()


@dp.message_handler(state=ProfileCreateCompetStatesGroup.add_compet_databegin)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["databegin"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите дату конца конкурса в формате xx.xx.xxxx")
    await ProfileCreateCompetStatesGroup.add_compet_dataEnd.set()


@dp.message_handler(state=ProfileCreateCompetStatesGroup.add_compet_dataEnd)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["dataend"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите дату конца приёма документов в формате xx.xx.xxxx")
    await ProfileCreateCompetStatesGroup.add_compet_deadline.set()


@dp.message_handler(state=ProfileCreateCompetStatesGroup.add_compet_deadline)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["datadeadline"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите срок реализации, если не предусмотрен пишите '-'")
    await ProfileCreateCompetStatesGroup.add_compet_place.set()


@dp.message_handler(state=ProfileCreateCompetStatesGroup.add_compet_place)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["place"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите сумму вознаграждени, если нет то '-'")
    await ProfileCreateCompetStatesGroup.add_compet_value.set()


@dp.message_handler(state=ProfileCreateCompetStatesGroup.add_compet_value)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["value"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите ссылку на конкурс")
    await ProfileCreateCompetStatesGroup.add_compet_sitelink.set()


@dp.message_handler(state=ProfileCreateCompetStatesGroup.add_compet_sitelink)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["sitelink"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы успешно зарегистрировали мероприятие!")
    await bot.send_message(chat_id=message.from_user.id,
                           text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                           reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileCreateMeroStatesGroup.add_mero_name)
async def add_name_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["title"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введите дату начала в формате xx.xx.xxxx ')
    await ProfileCreateMeroStatesGroup.add_mero_databegin.set()


@dp.message_handler(state=ProfileCreateMeroStatesGroup.add_mero_databegin)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["databegin"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите дату конца мероприятия в формате xx.xx.xxxx")
    await ProfileCreateMeroStatesGroup.add_mero_dataEnd.set()


@dp.message_handler(state=ProfileCreateMeroStatesGroup.add_mero_dataEnd)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["dataend"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите дату конца приёма документов в формате xx.xx.xxxx")
    await ProfileCreateMeroStatesGroup.add_mero_deadline.set()


@dp.message_handler(state=ProfileCreateMeroStatesGroup.add_mero_deadline)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["datadeadline"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите место проведения мероприятия в формате 'Город,Страна'")
    await ProfileCreateMeroStatesGroup.add_mero_place.set()


@dp.message_handler(state=ProfileCreateMeroStatesGroup.add_mero_place)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["place"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите ссылку на мероприятие")
    await ProfileCreateMeroStatesGroup.add_mero_sitelink.set()


@dp.message_handler(state=ProfileCreateMeroStatesGroup.add_mero_sitelink)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["sitelink"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы успешно зарегистрировали мероприятие!")
    await bot.send_message(chat_id=message.from_user.id,
                           text="Используя кнопки под этим сообщением можно управлять мероприятиями",
                           reply_markup=inline_admin_management_kb())
    await ProfileCreateMeroStatesGroup.admin.set()


@dp.message_handler(state=ProfileManagerLoginStatesGroup.manager_login_name)
async def state_manager_login_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Теперь введи фамилию")
    await ProfileManagerLoginStatesGroup.manager_login_surname.set()


@dp.message_handler(state=ProfileManagerLoginStatesGroup.manager_login_surname)
async def state_manager_login_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Теперь введи отчество")
    await ProfileManagerLoginStatesGroup.manager_login_patronymic.set()


@dp.message_handler(state=ProfileManagerLoginStatesGroup.manager_login_patronymic)
async def state_manager_login_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['patronymic'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Теперь введи идентификационный номер")
    await ProfileManagerLoginStatesGroup.manager_login_id.set()


@dp.message_handler(state=ProfileManagerLoginStatesGroup.manager_login_id)
async def state_manager_login_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    if data["id"] == config.ID:  # тут должно быть сравнение с записанными в бд данными админа
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отлично, я помню тебя!")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Добро пожаловать в личный кабинет!",
                               reply_markup=lk_manager_kb())
        await state.finish()
        await ProfileMenuGroup.menu_state.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Кажется ты ввёл неправильные данные или не зарегестрирован",
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                                   KeyboardButton('Зарегистрироваться'), KeyboardButton('Повторить ввод данных')))
        await state.finish()


@dp.message_handler(lambda message: message.text == "Меню", state=ProfileMenuGroup.menu_back)
async def menu_back(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id
                           , text="Добро пожаловать в личный кабинет!",
                           reply_markup=lk_manager_kb())
    await ProfileMenuGroup.menu_state.set()


def startup():
    print('Я живой')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=startup())
