import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from functions import agr_num_generator, get_day, get_month, get_year, generate_pdf_with_data
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class RegistrationState(StatesGroup):
    """Create dialog states"""

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
    """Start handler"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_registration = types.KeyboardButton('Почати')
    keyboard.add(button_registration)
    
    await message.answer('Привіт!'
                         '\nЯ Agreement Bot'
                         '\nЯ тут для того, щоб допомогти тобі у складанні '
                         'договору на навчання у ProgAcademy.'
                         '\nДля генерування договору натисни кнопку "Почати" '
                         'та слідуй моїм інструкціям',
                          reply_markup=keyboard)


@dp.message_handler(content_types=['text'], text='Почати')
async def handle_registration(message: types.Message, state: FSMContext):
    """Start dialog. Filling agreement number and creating date"""
    async with state.proxy() as data:
        data['edit_mode'] = False
        data['agreement_num'] = agr_num_generator(message.from_id)  
        data['sign_date'] = {'day' : get_day(),
                             'month': get_month(),
                             'year': get_year()}

    await message.answer('Введи своє ПІБ')
    await RegistrationState.NAME.set()
    
@dp.message_handler(state=RegistrationState.NAME)
async def handle_name(message: types.Message, state: FSMContext):
    """Name handler"""
    async with state.proxy() as data:
        data['name'] = message.text

    if data['edit_mode']:
        await RegistrationState.CHECK.set()
        await check(message, state)
    else:      
        await message.answer(f'Приємно познайомитись, {message.text}!'
                             '\nБудь ласка, введи серію паспорту:')
        await RegistrationState.PASSPORT_SER.set()
   

@dp.message_handler(state=RegistrationState.PASSPORT_SER)
async def handle_passport_ser(message: types.Message, state: FSMContext):
    """passport serial handler"""
    async with state.proxy() as data:
        data['passport_ser'] = message.text
    
    if data['edit_mode']:
        await RegistrationState.CHECK.set()
        await check(message, state)
    else:
        await message.answer('А тепер введи номер паспорту:')
        await RegistrationState.PASSPORT_NUM.set()


@dp.message_handler(state=RegistrationState.PASSPORT_NUM)
async def handle_passport_num(message: types.Message, state: FSMContext):
    """passport number handler"""
    async with state.proxy() as data:
        data['passport_num'] = message.text
    
    if data['edit_mode']:
        await RegistrationState.CHECK.set()
        await check(message, state)
    else:
        await message.answer('Наступною необхідно ввести інформацію '
                             'ким і коли був видан паспорт:')
        await RegistrationState.PASSPORT_ISSUED.set()
    

@dp.message_handler(state=RegistrationState.PASSPORT_ISSUED)
async def handle_passport_issued(message: types.Message, state: FSMContext):
    """Passport information handler"""
    async with state.proxy() as data:
        data['passport_issued_by'] = message.text
        
    if data['edit_mode']:
        await RegistrationState.CHECK.set()
        await check(message, state)
    else:        
        await message.answer('Будь ласка, вкажи адресу реестрації')
        await RegistrationState.REG_ADDRESS.set()


@dp.message_handler(state=RegistrationState.REG_ADDRESS)
async def handle_reg_address(message: types.Message, state: FSMContext):
    """Registration address handler"""
    async with state.proxy() as data:
        data['reg_address'] = message.text
    
    if data['edit_mode']:
        await RegistrationState.CHECK.set()
        await check(message, state)
    else:    
        await message.answer(f'Дякую! Ми майже закінчили, '
                             'залишилось зовсім трошки.'
                             '\nПрошу ввести свій ІПН:')
        await RegistrationState.ID_CODE.set()


@dp.message_handler(state=RegistrationState.ID_CODE)
async def handle_id_code(message: types.Message, state: FSMContext):
    """ID code handler"""
    async with state.proxy() as data:
        data['id_code'] = message.text
    
    if data['edit_mode']:
        await RegistrationState.CHECK.set()
        await check(message, state)
    else:   
        await message.answer(f'А на останок, будь ласка, вкажи '
                             'контактний номер телефону:')
        await RegistrationState.MOBILE_PHONE.set()


@dp.message_handler(state=RegistrationState.MOBILE_PHONE)
async def handle_phone(message: types.Message, state: FSMContext):
    """Phone number handler"""
    async with state.proxy() as data:
        data['mobile_phone'] = message.text

    if data['edit_mode']:
        await RegistrationState.CHECK.set()
        await check(message, state)
    else:    
        await RegistrationState.CHECK.set()
        await check(message, state)


@dp.message_handler(state=RegistrationState.CHECK)
async def check(message: types.Message, state: FSMContext):
    """Check inputed information"""
    async with state.proxy() as data:
        pass

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_edit_name = types.KeyboardButton(text='Редагувати ім\'я',
                                            value='edit_name' )
    button_edit_ps_ser = types.KeyboardButton('Редагувати серію паспорту')
    button_edit_ps_num = types.KeyboardButton('Редагувати номер паспорту')
    button_edit_issue = types.KeyboardButton('Редагувати орган видачі')
    button_edit_reg_address = types.KeyboardButton('Редагувати адресу реестрації')
    button_edit_id = types.KeyboardButton('Редагувати ІПН')
    button_edit_phone = types.KeyboardButton('Редагувати номер телефону')
    button_generation = types.KeyboardButton('Підтвердити')
    keyboard.add(button_edit_name, button_edit_ps_ser, button_edit_ps_num,
                 button_edit_issue, button_edit_reg_address, button_edit_id,
                 button_edit_phone, button_generation)

    await message.answer(f'Будь ласка, перевір введені дані.'
                         'За необхідності, можеш їх редагувати.'
                         '\nЯкщо все вірно, натисни "Підтвердити" '
                         'для генерації договору \n'
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
    """Edit information handler"""
    async with state.proxy() as data:
        data['edit_mode'] = True

    if message.text == 'Редагувати ім\'я':
        await message.answer(f'Введи своє ПІБ:')
        await RegistrationState.NAME.set()
    elif message.text == 'Редагувати серію паспорту':
        await message.answer(f'Введи серію паспорту:')
        await RegistrationState.PASSPORT_SER.set()
    elif message.text == 'Редагувати номер паспорту':
        await message.answer(f'Введи номер паспорту:')
        await RegistrationState.PASSPORT_NUM.set()
    elif message.text == 'Редагувати орган видачі':
        await message.answer(f'Введи ким і коли був видан паспорт:')
        await RegistrationState.PASSPORT_ISSUED.set()
    elif message.text == 'Редагувати адресу реестрації':
        await message.answer(f'Введи адресу реестрації:')
        await RegistrationState.REG_ADDRESS.set()
    elif message.text == 'Редагувати ІПН':
        await message.answer(f'Введи ІПН:')
        await RegistrationState.ID_CODE.set()
    elif message.text == 'Редагувати номер телефону':
        await message.answer(f'Введи свій номер телефону')
        await RegistrationState.MOBILE_PHONE.set()                    
    elif message.text == 'Підтвердити':
        await handle_registration(message, state)
    else:
        await check(message, state)


@dp.message_handler(state=RegistrationState.CONFIRMATION)
async def handle_registration(message: types.Message, state: FSMContext):
    """Generate file and send it to user"""
    async with state.proxy() as data:
        pass

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('/start')
    keyboard.add(button_start)
    
    html_file = './template/agreement_template.html'
    output_pdf = f'./agreements/agreement_{data["agreement_num"]}.pdf'
    generate_pdf_with_data(html_file, output_pdf, dict(data))

    await state.finish()
    await bot.send_document(message.chat.id, document=open(output_pdf, 'rb'))
    await message.answer('Дякую! Договір згенеровано.'
                         '\nБажаю гарного дня!'
                         '\n\nЩоб почати заново, введи "/start"',
                          reply_markup=keyboard)

if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling())
    except KeyboardInterrupt:
        asyncio.run(dp.stop_polling())

