from aiogram import types
from aiogram.dispatcher import FSMContext
import data.cityDb as db
import data.init_tables as sas
from loader import dp
from states.OrderData import AddCity




@dp.message_handler(commands="add_city")
async def create_city(message: types.Message):
    await message.answer("Shahar nomini kiriting.")
    await AddCity.name.set()



@dp.message_handler(state=AddCity.name)
async def process_city_creation(message: types.Message, state: FSMContext):
    name = message.text.strip()
    
    async with sas.AsyncSessionLocal() as session:
        new_city = await db.create_city(session, name)
    
    await message.answer(f"✅, Shahar `{new_city.name}` muvaffaqiyatli qoshildi") 