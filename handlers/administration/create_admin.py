from aiogram import types
from aiogram.dispatcher import FSMContext
import utils.db_api.administrationDb as db
from loader import dp
from states.adminData import AdminData, AdminDeletion
import utils.db_api.init_tables as sas
from states.state_finish import safe_state_finish




@dp.message_handler(commands="add_admin", state="*")
async def add_admin_handler(mas: types.Message, state: FSMContext):
    # If user was in another state, cancel it
    await safe_state_finish(state)
    await mas.answer("Admin ismini kiriting.")
    await AdminData.name.set()


@dp.message_handler(state=AdminData.name)
async def get_name(mas: types.Message, state: FSMContext):
    await state.update_data(name=mas.text)
    await mas.answer("Adminning account_id sini kiriting:")
    await AdminData.account_id.set()


@dp.message_handler(state=AdminData.account_id)
async def get_account_id(mas: types.Message, state: FSMContext):
    try:
        account_id = int(mas.text.strip())
    except ValueError:
        await mas.answer("❌ account_id faqat son bo‘lishi kerak.")
        return

    await state.update_data(account_id=account_id)
    data = await state.get_data()

    name = data.get("name", "Nomalum")
    account_id = data.get("account_id")

    await mas.answer(
        f"✅ Admin ma’lumotlari:\n\n"
        f"👤 Ism: {name}\n"
        f"🆔 account_id: {account_id}"
    )

    async with sas.AsyncSessionLocal() as session:
        admin_data = await db.create_admin(session, account_id, name)
        await mas.answer(
            f"✅ Ro‘yxatdan o‘tish yakunlandi!\n\n"
            f"ID: {admin_data.id}\n"
            f"Ism: {admin_data.name}\n"
            f"Account ID: {admin_data.account_id}"
        )

    await safe_state_finish(state)
    
    
    


@dp.message_handler(commands="admins", state="*")
async def admin_list(mas: types.Message, state: FSMContext):
    # Cancel any previous state
    await safe_state_finish(state)
    
    await mas.answer("🔎 Admin ismini kiriting.")
    await AdminDeletion.form.set()


# --- Handler: get admin by name ---
@dp.message_handler(state=AdminDeletion.form)
async def get_admin_handler(mas: types.Message, state: FSMContext):   
    name = mas.text.strip()

    async with sas.AsyncSessionLocal() as session:
        admin_data = await db.get_admin(session, name)

    if not admin_data:
        await mas.answer(f"❌ '{name}' nomli admin topilmadi.")
        return

    await mas.answer(
        f"✅ Admin ma’lumotlari:\n"
        f"ID: <b>{admin_data.id}</b>\n"
        f"👤 Ism: <b>{admin_data.name}</b>\n"
        f"🆔 account_id (owner ID): <b>{admin_data.account_id}</b>",
        parse_mode="HTML"
    )

    await safe_state_finish(state)
