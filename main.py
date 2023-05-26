import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN = "5670993457:AAFAL0_TFVTIVz5EYgiGz8WRI9BjWenLWoY"

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

class RegistrationState(StatesGroup):
    NAME = State()
    DATE_OF_BIRTH = State()


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    # Відправляємо привітальне повідомлення
    await message.answer("Привіт! Я бот. Я можу зареєструвати тебе.")
    
    # Створюємо клавіатуру з кнопкою "Реєстрація"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_registration = types.KeyboardButton("Реєстрація")
    keyboard.add(button_registration)
    
    # Відправляємо клавіатуру користувачу
    await message.answer("Натисни кнопку Реєстрація, щоб продовжити.", reply_markup=keyboard)


@dp.message_handler(content_types=['text'], text="Реєстрація")
async def handle_registration(message: types.Message):
    # Обробка натиснення кнопки "Реєстрація"

    await message.answer("Ти обрав реєстрацію. Введи своє ім'я.")
    # Тут можна продовжити обробку введення імені та збереження даних користувача

    # Встановлюємо стан "Очікування імені"
    await RegistrationState.NAME.set()


@dp.message_handler(state=RegistrationState.NAME)
async def handle_name(message: types.Message, state: FSMContext):
    # Обробка введення імені

    async with state.proxy() as data:
        data['agreement_num'] = '123'   
        data['name'] = message.text
    print(message)
    # Відправляємо привітання з ім'ям користувача
    await message.answer(f"Привіт, {message.text}! Тепер введи свою дату народження (у форматі ДД-ММ-РРРР).")
    # Встановлюємо стан "Очікування дати народження"
    await RegistrationState.DATE_OF_BIRTH.set()


@dp.message_handler(state=RegistrationState.DATE_OF_BIRTH)
async def handle_date_of_birth(message: types.Message, state: FSMContext):
    # Обробка введення дати народження
    async with state.proxy() as data:
        data['date_of_birth'] = message.text
    
    # Отримуємо дані з контексту
    async with state.proxy() as data:
        name = data['name']
        date_of_birth = data['date_of_birth']
    
    print(data)

    # Відправляємо підтвердження разом із введеними даними
    await message.answer(f"Дякуємо! Твоє ім'я: {name}, Дата народження: {date_of_birth}")

    # Видаляємо дані користувача
    await state.finish()


if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling())
    except KeyboardInterrupt:
        asyncio.run(dp.stop_polling())

