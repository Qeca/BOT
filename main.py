from config import TOKEN_API
from aiogram import Dispatcher, Bot, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, InputFile, WebAppInfo
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import get_start_kb, get_company_kb, lk_manager_kb, inline_driver_management_kb, get_drivers_kb, \
    inline_company_management_kb, inline_vehicle_control_kb
from aiogram.dispatcher import FSMContext
from model.Manager import Manager
from repository import CompanyRepository, UserRepository

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


class ProfileDriverManagementGroup(StatesGroup):
    driver = State()
    show_driver = State()
    add_driver_name = State()
    add_driver_surname = State()
    add_driver_company = State()
    del_driver = State()
    del_driver_complete = State()
    link_car_to_driver = State()
    link_car_to_driver_driver = State()
    show_driver_on_road = State()


class ProfileManagerLoginStatesGroup(StatesGroup):
    manager_login_name = State()
    manager_login_surname = State()


class ProfileManagerStatesGroup(StatesGroup):
    manager_reg_name = State()
    manager_reg_surname = State()


class ProfileCompanyStatesGroup(StatesGroup):
    company_reg_name = State()
    change_company = State()
    company = State()


class ProfileVehicleControlStatesGroup(StatesGroup):
    vehicle = State()
    add_vehicle_gos = State()
    add_vehicle_mark = State()
    add_vehicle_model = State()
    del_vehicle = State()
    link_veh = State()
    back_veh = State()


@dp.message_handler(lambda message: message.text == "Управление компанией", state=ProfileMenuGroup.menu_state)
async def company_management(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Твоя компания: (тут должна быть компания менеджера)",
                           reply_markup=inline_company_management_kb())
    await state.finish()
    await ProfileCompanyStatesGroup.company.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "back_w",
                           state=ProfileCompanyStatesGroup.company)
async def back_w(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer(text="Добро пожаловать в личный кабинет!",
                                  reply_markup=lk_manager_kb())
    await ProfileMenuGroup.menu_state.set()


@dp.message_handler(lambda message: message.text == "Управление машинами", state=ProfileMenuGroup.menu_state)
async def vehicle_control(message: types.Message, state: FSMContext):
    k = f'Все машины:\n'
    for i in range(len(dict_vehicle['name'])):
        k += f'{dict_vehicle["name"][i]} : {dict_vehicle["state"][i]}\n'
    await bot.send_message(chat_id=message.from_user.id,
                           text=k,
                           reply_markup=inline_vehicle_control_kb())
    await state.finish()
    await ProfileVehicleControlStatesGroup.vehicle.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "back",
                           state=ProfileVehicleControlStatesGroup.vehicle)
async def back(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer(text="Добро пожаловать в личный кабинет!",
                                  reply_markup=lk_manager_kb())
    await ProfileMenuGroup.menu_state.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "del_vehicle",
                           state=ProfileVehicleControlStatesGroup.vehicle)
async def veh_add(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введите гос номер машины")
    await ProfileVehicleControlStatesGroup.del_vehicle.set()


@dp.message_handler(state=ProfileVehicleControlStatesGroup.del_vehicle)
async def veh_add_gos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['del_number'] = message.text
    # тут удаление
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы успешно удалили автомобиль")
    k = f'Все машины:\n'
    for i in range(len(dict_vehicle['name'])):
        k += f'{dict_vehicle["name"][i]} : {dict_vehicle["state"][i]}\n'
    await bot.send_message(chat_id=message.from_user.id,
                           text=k,
                           reply_markup=inline_vehicle_control_kb())
    await state.finish()
    await ProfileVehicleControlStatesGroup.vehicle.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "add_vehicle",
                           state=ProfileVehicleControlStatesGroup.vehicle)
async def veh_add(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введите гос номер машины")
    await ProfileVehicleControlStatesGroup.add_vehicle_gos.set()


@dp.message_handler(state=ProfileVehicleControlStatesGroup.add_vehicle_gos)
async def veh_add_gos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['transportNumber'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите марку автомобиля")
    await ProfileVehicleControlStatesGroup.add_vehicle_mark.set()


@dp.message_handler(state=ProfileVehicleControlStatesGroup.add_vehicle_mark)
async def veh_add_gos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mark'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите модель автомобиля")
    await ProfileVehicleControlStatesGroup.add_vehicle_model.set()


@dp.message_handler(state=ProfileVehicleControlStatesGroup.add_vehicle_model)
async def veh_add_gos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы успешно зарегестрировали автомобиль")
    k = f'Все машины:\n'
    for i in range(len(dict_vehicle['name'])):
        k += f'{dict_vehicle["name"][i]} : {dict_vehicle["state"][i]}\n'
    await bot.send_message(chat_id=message.from_user.id,
                           text=k,
                           reply_markup=inline_vehicle_control_kb())
    await state.finish()
    await ProfileVehicleControlStatesGroup.vehicle.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "change_company",
                           state=ProfileCompanyStatesGroup.company)
async def change_company(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text="Выберите нужную команию",
                                  reply_markup=get_drivers_kb(dict_company["name"]))
    await ProfileCompanyStatesGroup.change_company.set()


@dp.message_handler(state=ProfileCompanyStatesGroup.change_company)
async def change_company_last(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["company_id"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы успешно выбрали компанию')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Твоя компания: (тут должна быть компания менеджера)",
                           reply_markup=inline_company_management_kb())
    await state.finish()
    await ProfileCompanyStatesGroup.company.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "reg_company",
                           state=ProfileCompanyStatesGroup.company)
async def reg_company(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Введите название компании")
    await ProfileCompanyStatesGroup.company_reg_name.set()


@dp.message_handler(state=ProfileCompanyStatesGroup.company_reg_name)
async def reg_company_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["company_name"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы успешно зарегестрировали компанию')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Твоя компания: (тут должна быть компания менеджера)",
                           reply_markup=inline_company_management_kb())
    await state.finish()
    await ProfileCompanyStatesGroup.company.set()


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


@dp.message_handler(lambda message: message.text == "Меню", state=ProfileMenuGroup.menu_back)
async def menu_back(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id
                           , text="Добро пожаловать в личный кабинет!",
                           reply_markup=lk_manager_kb())
    await ProfileMenuGroup.menu_state.set()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в нашего бота! Пожалуйста сообщи кто ты :)',
                           reply_markup=get_start_kb())
    await message.delete()


@dp.message_handler(lambda message: message.text in ['Я менеджер!', 'Я водитель!'])
async def driver_or_manager(message: types.Message) -> None:
    if message.text == "Я менеджер!":
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


@dp.message_handler(state=ProfileMenuGroup.menu_state)
async def driver_management(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text == "Управление водителями":
        await bot.send_message(chat_id=message.from_user.id, text="Переходим к управлению водителями")
        drivers = CompanyRepository.getDriversByCompany(companyId="5123")

        data = f"Все водители в компании:\n"
        for driver in drivers:
            data += f"{driver.id} {driver.lastname} {driver.firstname} \n"

        await bot.send_message(chat_id=message.from_user.id,
                               text=data,
                               reply_markup=inline_driver_management_kb())
        await ProfileDriverManagementGroup.driver.set()


@dp.message_handler(state=ProfileDriverManagementGroup.add_driver_company)
async def add_company_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["company"] = message.text
    await state.finish()
    c_id = dict_managers["company_id"][dict_managers["lastname"].index(f'{dict_login_manager["lastname"]}')]
    await bot.send_message(chat_id=message.from_user.id,
                           text="Ты успешно зарегистрировал водителя")
    datas = f"Все водители в компании:\n"
    for i in range(len(dict_drivers["lastname"])):
        if dict_drivers['company_id'][i] == c_id:
            datas += f"{dict_drivers['firstname'][i]} {dict_drivers['lastname'][i]}\n"
    await bot.send_message(chat_id=message.from_user.id,
                           text=datas,
                           reply_markup=inline_driver_management_kb())
    await state.finish()
    await ProfileDriverManagementGroup.driver.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'show_driver_on_road',
                           state=ProfileDriverManagementGroup.driver)
async def link_car_to_driver(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    k = f'Все водители в пути:\n'
    for i in range(len(dict_drivers['firstname'])):
        if dict_drivers['state'][i] == "В пути":
            k += f'{dict_drivers["firstname"][i]} {dict_drivers["lastname"][i]}\n'
    await callback.message.edit_text(text=k,
                                     reply_markup=inline_driver_management_kb())
    await state.finish()
    await ProfileDriverManagementGroup.driver.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "back",
                           state=ProfileDriverManagementGroup.driver)
async def back(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer(text="Добро пожаловать в личный кабинет!",
                                  reply_markup=lk_manager_kb())
    await ProfileMenuGroup.menu_state.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'link_car_to_driver',
                           state=ProfileDriverManagementGroup.driver)
async def link_car_to_driver_vehicle(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Переходим к привязке машин к водителям')
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="Вот список машин",
                           reply_markup=get_drivers_kb(list_vehicle))
    await ProfileDriverManagementGroup.link_car_to_driver.set()


@dp.message_handler(state=ProfileDriverManagementGroup.link_car_to_driver)
async def link_car_to_driver_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["vehicle"] = message.text
    await bot.send_message(chat_id=message.chat.id,
                           text="Вот список людей",
                           reply_markup=get_drivers_kb(list_drivers))
    await ProfileDriverManagementGroup.link_car_to_driver_driver.set()


@dp.message_handler(state=ProfileDriverManagementGroup.link_car_to_driver_driver)
async def link_car_to_driver_end(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["driver"] = message.text
    c_id = dict_managers["company_id"][dict_managers["lastname"].index(f'{dict_login_manager["lastname"]}')]
    await bot.send_message(chat_id=message.from_user.id,
                           text="Ты успешно привязал машину к водителю")
    datas = f"Все водители в компании:\n"
    for i in range(len(dict_drivers["lastname"])):
        if dict_drivers['company_id'][i] == c_id:
            datas += f"{dict_drivers['firstname'][i]} {dict_drivers['lastname'][i]}\n"
    await bot.send_message(chat_id=message.from_user.id,
                           text=datas,
                           reply_markup=inline_driver_management_kb())
    await state.finish()
    await ProfileDriverManagementGroup.driver.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'del_driver',
                           state=ProfileDriverManagementGroup.driver)
async def del_driver(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Переходим к удалению водителей')
    drivers = CompanyRepository.getDriversByCompany(companyId="5123")
    initials = []
    for driver in drivers:
        initials.append(f"{driver.id} {driver.lastname} {driver.firstname}")
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="Вот список водителей",
                           reply_markup=get_drivers_kb(initials))
    await ProfileDriverManagementGroup.del_driver_complete.set()


@dp.message_handler(state=ProfileDriverManagementGroup.del_driver_complete)
async def del_driver_complete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delete_driver'] = message.text
    await state.finish()

    id = data['delete_driver'].split(" ")[0]
    driver = UserRepository.deleteDriver(id)
    if driver.id == None:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Удаление {message.text} невозможно, пока водитель находится в поездке")
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Вы успешно удалили {message.text}")
    drivers = CompanyRepository.getDriversByCompany(companyId="5123")

    data = f"Все водители в компании:\n"
    for driver in drivers:
        data += f"{driver.id} {driver.lastname} {driver.firstname} \n"
    await bot.send_message(chat_id=message.from_user.id,
                           text=data,
                           reply_markup=inline_driver_management_kb())
    await ProfileDriverManagementGroup.driver.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'add_driver',
                           state=ProfileDriverManagementGroup.driver)
async def add_driver(callback: types.CallbackQuery, state: FSMContext):
    a = await callback.message.edit_text(text="Переходим к добавлению водителя, напишите его имя")
    await ProfileDriverManagementGroup.add_driver_name.set()


@dp.message_handler(state=ProfileDriverManagementGroup.add_driver_name)
async def add_name_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["firstname"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text='Теперь введи фамилию')
    await ProfileDriverManagementGroup.add_driver_surname.set()


@dp.message_handler(state=ProfileDriverManagementGroup.add_driver_surname)
async def add_surname_driver(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["lastname"] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введи название комании к которой будет привязан водитель")
    await ProfileDriverManagementGroup.add_driver_company.set()


@dp.message_handler(state=ProfileManagerLoginStatesGroup.manager_login_name)
async def state_manager_login_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Теперь введи фамилию")
    await ProfileManagerLoginStatesGroup.next()


@dp.message_handler(state=ProfileManagerLoginStatesGroup.manager_login_surname)
async def state_manager_login_surname(message: types.Message, state: FSMContext):
    global dict_login_manager
    async with state.proxy() as data:
        data['lastname'] = message.text
    dict_login_manager = data
    if proverka_dostupa(data):
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


@dp.message_handler(state=ProfileManagerStatesGroup.manager_reg_name)
async def state_manager_reg_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text

    await bot.send_message(chat_id=message.from_user.id, text='Теперь введи свою фамилию')
    await ProfileManagerStatesGroup.next()


@dp.message_handler(state=ProfileManagerStatesGroup.manager_reg_surname)
async def state_manager_req_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text
        manager: Manager = Manager(message.from_user.id, data['firstname'], data['lastname'])
        add_manager = UserRepository.addManager(manager)

    dict_managers['firstname'].append(data['firstname']), dict_managers['lastname'].append(data['lastname'])
    print(add_manager)
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Ты успешно зарегестрировался")
    await bot.send_message(chat_id=message.from_user.id,
                           text="Добро пожаловать в личный кабинет!",
                           reply_markup=lk_manager_kb())


def proverka_dostupa(dictionary: dict) -> bool:
    if dictionary['firstname'] in dict_managers['firstname'] and dictionary['lastname'] in dict_managers['lastname'] and \
            dict_managers['firstname'].index(dictionary['firstname']) == dict_managers['lastname'].index(
        dictionary['lastname']):
        return True
    else:
        return False


def startup():
    print('Я живой')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=startup())
