from aiogram import types
from aiogram.dispatcher import FSMContext

import utils.db_api.cityDb as db
import utils.db_api.init_tables as sas
from loader import dp
from states.cityData import CityUpdate
from states.state_finish import safe_state_finish
from filters import IsSuperUser


@dp.message_handler(IsSuperUser(), commands="update_city")
async def start_update(message: types.Message):
    await message.answer("Shahar nomini kiriting (eski nom).")
    await CityUpdate.name.set()


@dp.message_handler(IsSuperUser(), state=CityUpdate.name)
async def get_new_name(message: types.Message, state: FSMContext):
    old_name = message.text.strip()
    await state.update_data(old_name=old_name)

    await message.answer("Shahrning yangi nomini kiriting.")
    await CityUpdate.new_name.set()


@dp.message_handler(IsSuperUser(), state=CityUpdate.new_name)
async def update(message: types.Message, state: FSMContext):
    new_name = message.text.strip()
    data = await state.get_data()
    old_name = data.get("old_name")

    async with sas.AsyncSessionLocal() as session:
        city = await db.get_city_by_name(db=session, name=old_name)
        if not city:
            await message.answer(f"❌ Shahar '{old_name}' topilmadi.")
            await safe_state_finish(state)
            return

        updated_city = await db.update_city(session, city_id=city.id, name=new_name)

    await safe_state_finish(state)

    if updated_city:
        await message.answer(
            f"✅ Shahar nomi yangilandi:\n"
            f"Eski nom: <b>{old_name}</b>\n"
            f"Yangi nom: <b>{updated_city.name}</b>",
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Yangilash amalga oshmadi.")
