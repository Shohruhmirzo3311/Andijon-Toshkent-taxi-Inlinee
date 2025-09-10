from aiogram import types
from aiogram.dispatcher import FSMContext

import utils.db_api.cityDb as db
import utils.db_api.init_tables as sas
from loader import dp
from states.cityData import CityDel
from states.state_finish import safe_state_finish
from filters import IsSuperUser

@dp.message_handler(IsSuperUser(), commands="delete_city", state="*")
async def delete_city(mas: types.Message):
    await mas.answer("Shahar nomini kiriting.")
    await CityDel.name.set()



@dp.message_handler(state=CityDel.name)
async def deletion_process(mas: types.Message, state: FSMContext):
    city_name = mas.text.strip()
    
    async with sas.AsyncSessionLocal() as session:
        deleted_city = await db.delete_city(session, city_name)
    
    await safe_state_finish(state)

    if deleted_city:
        await mas.answer(f"✅ Shahar `{deleted_city.name}` muvaffaqiyatli o'chirildi")
    else:
        await mas.answer(f"❌ `{city_name}` nomli shahar topilmadi")