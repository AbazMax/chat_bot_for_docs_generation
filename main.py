import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from functions import agr_num_generator, get_day, get_month, get_year, generate_pdf_with_data

TOKEN = "5670993457:AAFAL0_TFVTIVz5EYgiGz8WRI9BjWenLWoY"

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
    CONFIRMATION = State()

@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    # Відправляємо привітальне повідомлення
    await message.answer("Привіт! Для складання договору, будь ласка, введи свої дані")
    
    # Створюємо клавіатуру з кнопкою "Реєстрація"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_registration = types.KeyboardButton("Почати")
    keyboard.add(button_registration)
    
    # Відправляємо клавіатуру користувачу
    await message.answer('Натисни кнопку "Почати", та слідуй інструкції.', reply_markup=keyboard)


@dp.message_handler(content_types=['text'], text="Почати")
async def handle_registration(message: types.Message):
    # Обробка натиснення кнопки "Реєстрація"

    await message.answer("Введи своє ПІБ")
    # Тут можна продовжити обробку введення імені та збереження даних користувача

    # Встановлюємо стан "Очікування імені"
    await RegistrationState.NAME.set()


@dp.message_handler(state=RegistrationState.NAME)
async def handle_name(message: types.Message, state: FSMContext):
    # Обробка введення імені

    async with state.proxy() as data:
        data['agreement_num'] = agr_num_generator(message.from_id)  
        data['name'] = message.text
        data['sign_date'] = {'day' : get_day(),
                             'month': get_month(),
                             'year': get_year()}
        
    # Відправляємо привітання з ім'ям користувача
    await message.answer(f"Привіт, {message.text}! Тепер введи серію паспорту.")
    # Встановлюємо стан "Очікування дати народження"
    await RegistrationState.PASSPORT_SER.set()


@dp.message_handler(state=RegistrationState.PASSPORT_SER)
async def handle_passport_ser(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        data['passport_ser'] = message.text
    
    
    
    # Відправляємо підтвердження разом із введеними даними
    # await message.answer(f"Дякуємо! Твоє ім'я: {name}, Дата народження: {passport_ser}")
    await message.answer(f"Введи номер паспорту")
    await RegistrationState.PASSPORT_NUM.set()


@dp.message_handler(state=RegistrationState.PASSPORT_NUM)
async def handle_passport_num(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        data['passport_num'] = message.text
    
    await message.answer(f"Дякую! Тепер введи ким і коли був видан паспорт")
    await RegistrationState.PASSPORT_ISSUED.set()
    

@dp.message_handler(state=RegistrationState.PASSPORT_ISSUED)
async def handle_passport_issued(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        data['passport_issued_by'] = message.text
    
    await message.answer(f"Далі введи адрес реестрації")
    await RegistrationState.REG_ADDRESS.set()


@dp.message_handler(state=RegistrationState.REG_ADDRESS)
async def handle_reg_address(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        data['reg_address'] = message.text
    
    await message.answer(f"Тепер, будь ласка, введи свій ІПН")
    await RegistrationState.ID_CODE.set()


@dp.message_handler(state=RegistrationState.ID_CODE)
async def handle_id_code(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        data['id_code'] = message.text
    
    await message.answer(f"Вкажи свій номер телефону")
    await RegistrationState.MOBILE_PHONE.set()


@dp.message_handler(state=RegistrationState.MOBILE_PHONE)
async def handle_phone(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        data['mobile_phone'] = message.text


    # Створюємо клавіатуру з кнопкою "Генерувати"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_generation = types.KeyboardButton("Генерувати")
    keyboard.add(button_generation)

    await message.answer(f"Дякую, дані прийняті.{data}", reply_markup=keyboard)
    await RegistrationState.CONFIRMATION.set()


@dp.message_handler(content_types=['text'], text="Генерувати", state=RegistrationState.CONFIRMATION)
async def handle_registration(message: types.Message, state: FSMContext):
    # Обробка натиснення кнопки "Реєстрація"

    # Отримуємо дані з контексту
    async with state.proxy() as data:
        pass
    
    html_file = './template/agreement_template.html'
    output_pdf = './agreements/output.pdf'
    generate_pdf_with_data(html_file, output_pdf, dict(data))

    print(dict(data))
    await message.answer(f"Договір сгенеровано...{dict(data)}")    

    # Видаляємо дані користувача
    await state.finish()

if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling())
    except KeyboardInterrupt:
        asyncio.run(dp.stop_polling())

