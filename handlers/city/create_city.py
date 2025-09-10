from aiogram import types
from aiogram.dispatcher import FSMContext

import utils.db_api.cityDb as db
import utils.db_api.init_tables as sas
from loader import dp
from states.cityData import City
from states.state_finish import safe_state_finish
from filters import IsSuperUser


@dp.message_handler(IsSuperUser(), commands="add_city")
async def create_city(message: types.Message):
    await message.answer("Shahar nomini kiriting.")
    await City.name.set()



@dp.message_handler(state=City.name)
async def process_city_creation(message: types.Message, state: FSMContext):
    name = message.text.strip()
    
    async with sas.AsyncSessionLocal() as session:
        new_city = await db.create_city(session, name)
    
    await safe_state_finish(state)
    await message.answer(f"✅, Shahar `{new_city.name}` muvaffaqiyatli qoshildi") 
    

@dp.message_handler(IsSuperUser(), commands="cities")
async def cities_list(mas: types.Message):
    async with sas.AsyncSessionLocal() as session:
        cities = await db.get_all_cities(session)

    if not cities:
        await mas.answer("❌ Hali shaharlar mavjud emas.")
        return

    text = "🏙 Bizda mavjud shaharlar:\n\n"
    text += "\n".join(f"• {city}" for city in cities)

    await mas.answer(text)
