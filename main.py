import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from functions import agr_num_generator, get_day, get_month, get_year, generate_pdf_with_data

TOKEN = '5670993457:AAFAL0_TFVTIVz5EYgiGz8WRI9BjWenLWoY'

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class RegistrationState(StatesGroup):
    NAME = State()
    PASSPORT_SER = State()
    PASSPORT_NUM = State()
    PASSPORT_ISSUED = State()
    REG_ADDRESS = State()
    ID_CODE = State()
    MOBILE_PHONE = State()
    CHECK = State()
    CONFIRMATION = State()
    

@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    # start message
    
    # creating keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_registration = types.KeyboardButton('Почати')
    keyboard.add(button_registration)
    
    await message.answer('Привіт! Для складання договору, будь ласка, введи свої дані.'
                         '\nНатисни кнопку "Почати", та слідуй інструкції.', reply_markup=keyboard)


@dp.message_handler(content_types=['text'], text='Почати')
async def handle_registration(message: types.Message, state: FSMContext):
    # Обробка натиснення кнопки "Реєстрація"
    async with state.proxy() as data:
        data['edit_name'] = False
        data['edit_pass_ser'] = False
        data['edit_pass_num'] = False
        data['edit_pass_iss'] = False
        data['edit_reg_address'] = False
        data['edit_id_code'] = False
        data['edit_phone'] = False
        data['agreement_num'] = agr_num_generator(message.from_id)  
        data['sign_date'] = {'day' : get_day(),
                             'month': get_month(),
                             'year': get_year()}


    await message.answer('Введіть своє ПІБ')
    # Тут можна продовжити обробку введення імені та збереження даних користувача
    # Встановлюємо стан "Очікування імені"
    await RegistrationState.NAME.set()
    

@dp.message_handler(state=RegistrationState.NAME)
async def handle_name(message: types.Message, state: FSMContext):
    # Обробка введення імені
    async with state.proxy() as data:
        data['name'] = message.text

    if data['edit_name']:
        await RegistrationState.CHECK.set()
        await check(message, state)

    else:      
        await message.answer(f'Привіт, {message.text}! Тепер введи серію паспорту.')
        await RegistrationState.PASSPORT_SER.set()
   


@dp.message_handler(state=RegistrationState.PASSPORT_SER)
async def handle_passport_ser(message: types.Message, state: FSMContext):
    # passport serial handler
    async with state.proxy() as data:
        data['passport_ser'] = message.text
    
    await message.answer(f'Введи номер паспорту')
    await RegistrationState.PASSPORT_NUM.set()


@dp.message_handler(state=RegistrationState.PASSPORT_NUM)
async def handle_passport_num(message: types.Message, state: FSMContext):
    # passport number handler
    async with state.proxy() as data:
        data['passport_num'] = message.text
    
    await message.answer(f'Дякую! Тепер введи ким і коли був видан паспорт')
    await RegistrationState.PASSPORT_ISSUED.set()
    

@dp.message_handler(state=RegistrationState.PASSPORT_ISSUED)
async def handle_passport_issued(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['passport_issued_by'] = message.text
    
    await message.answer(f'Далі введи адрес реестрації')
    await RegistrationState.REG_ADDRESS.set()


@dp.message_handler(state=RegistrationState.REG_ADDRESS)
async def handle_reg_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['reg_address'] = message.text
    
    await message.answer(f'Тепер, будь ласка, введи свій ІПН')
    await RegistrationState.ID_CODE.set()


@dp.message_handler(state=RegistrationState.ID_CODE)
async def handle_id_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_code'] = message.text
    
    await message.answer(f'Вкажи свій номер телефону')
    await RegistrationState.MOBILE_PHONE.set()


@dp.message_handler(state=RegistrationState.MOBILE_PHONE)
async def handle_phone(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        data['mobile_phone'] = message.text

    await RegistrationState.CHECK.set()
    await check(message, state)

@dp.message_handler(state=RegistrationState.CHECK)
async def check(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        pass

    # creating keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_edit_name = types.KeyboardButton(text='Редагувати ім\'я', value='edit_name' )
    button_edit_ps_ser = types.KeyboardButton('Редагувати серію паспорту')
    button_edit_ps_num = types.KeyboardButton('Редагувати номер паспорту')
    button_edit_issue = types.KeyboardButton('Редагувати орган видачі')
    button_edit_reg_address = types.KeyboardButton('Редагувати адресу реестрації')
    button_edit_id = types.KeyboardButton('Редагувати ІПН')
    button_edit_phone = types.KeyboardButton('Редагувати номер телефону')
    button_generation = types.KeyboardButton('Підтвердити')
    keyboard.add(button_edit_name, button_edit_ps_ser, button_edit_ps_num, button_edit_issue,
                 button_edit_reg_address, button_edit_id, button_edit_phone, button_generation)

    await message.answer(f'Будь ласка, перевірте введені дані. За необхідності, можете їх редагувати.'
                         '\nЯкщо все вірно, натисніть "Підтвердити" для генерації договору \n'
                         f'\nПІБ: {data["name"]}'
                         f'\nСерія паспорту: {data["passport_ser"]}'
                         f'\nНомер паспорту: {data["passport_num"]}'
                         f'\nКим і коли видан: {data["passport_issued_by"]}'
                         f'\nАдреса реестрації: {data["reg_address"]}'
                         f'\nІПН: {data["id_code"]}'
                         f'\nНомер телефону: {data["mobile_phone"]}', 
                        reply_markup=keyboard)
    await RegistrationState.CONFIRMATION.set()


@dp.message_handler(state=RegistrationState.CONFIRMATION)
async def edit_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_name'] = True

    await message.answer(f'Будь ласка, введіть оновлене ПІБ')
    await RegistrationState.NAME.set()


@dp.message_handler(content_types=['text'], text='Підтвердити', state=RegistrationState.CONFIRMATION)
async def handle_registration(message: types.Message, state: FSMContext):

    # get data from context
    async with state.proxy() as data:
        pass
    
    html_file = './template/agreement_template.html'
    output_pdf = './agreements/output.pdf'
    generate_pdf_with_data(html_file, output_pdf, dict(data))

    print(dict(data))
    await message.answer(f'Договір сгенеровано...{dict(data)}')    

    # delete user data
    await state.finish()

if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling())
    except KeyboardInterrupt:
        asyncio.run(dp.stop_polling())

