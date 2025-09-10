from aiogram import types
from aiogram.dispatcher import FSMContext
import utils.db_api.administrationDb as db
from loader import dp
from states.adminData import AdminUpdate
import utils.db_api.init_tables as sas
from utils.db_api.administrationDb import Bot_Admin
from sqlalchemy import select, func
from states.state_finish import safe_state_finish


@dp.message_handler(commands="admin_update", state="*")
async def update_admin_start(mas: types.Message, state: FSMContext):
    await safe_state_finish(state)
    await mas.answer("🔎 O'zgartirmoqchi bo'lgan admin ismini kiriting:")
    await AdminUpdate.get_name.set()


@dp.message_handler(state=AdminUpdate.get_name)
async def get_admin_by_name(mas: types.Message, state: FSMContext):
    name = mas.text.strip()

    async with sas.AsyncSessionLocal() as session:
        result = await session.execute(
            select(Bot_Admin).where(func.lower(Bot_Admin.name) == name.lower())
        )
        admin_data = result.scalar_one_or_none()

    if not admin_data:
        await mas.answer(f"❌ '{name}' nomli admin topilmadi.")
        await safe_state_finish(state)
        return

    # Save admin_id in state
    await state.update_data(admin_id=admin_data.id)

    await mas.answer(
        f"✅ Admin topildi:\n"
        f"ID: <b>{admin_data.id}</b>\n"
        f"👤 Eski ism: <b>{admin_data.name}</b>\n\n"
        f"✏️ Yangi ismni kiriting:",
        parse_mode="HTML"
    )
    await AdminUpdate.new_name.set()


# --- Step 2: update admin ---
@dp.message_handler(state=AdminUpdate.new_name)
async def update_admin_handler(mas: types.Message, state: FSMContext):
    data = await state.get_data()
    admin_id = data.get("admin_id")
    new_name = mas.text.strip()

    async with sas.AsyncSessionLocal() as session:
        admin_data = await db.update_admin(session, admin_id, new_name)

    if not admin_data:
        await mas.answer("❌ Admin yangilashda xatolik yuz berdi.")
    else:
        await mas.answer(
            f"✅ Admin ma’lumotlari yangilandi:\n"
            f"ID: <b>{admin_data.id}</b>\n"
            f"👤 Yangi ism: <b>{admin_data.name}</b>\n"
            f"🆔 account_id: <b>{admin_data.account_id}</b>",
            parse_mode="HTML"
        )

    await safe_state_finish(state)