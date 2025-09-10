from aiogram import types
from aiogram.dispatcher import FSMContext
import utils.db_api.administrationDb as db
from loader import dp
from states.adminData import AdminDeletion
import utils.db_api.init_tables as sas
from states.state_finish import safe_state_finish



@dp.message_handler(commands="delete_admin", state="*")
async def delete_admin_command(mas: types.Message):
    await mas.answer("Adminning account_id sini kiriting.")
    await AdminDeletion.form.set()


@dp.message_handler(state=AdminDeletion.form)
async def deletion_process(mas: types.Message, state: FSMContext):
    try:
        account_id = int(mas.text.strip())
    except ValueError:
        await mas.answer("❌ account_id faqat son bo‘lishi kerak.")
        return

    async with sas.AsyncSessionLocal() as session:
        admin_data = await db.delete_admin(session, account_id)

        if not admin_data:
            await mas.answer("❌ Bunday admin topilmadi.")
        else:
            await mas.answer(
                f"🗑 Admin o‘chirildi!\n\n"
                f"ID: {admin_data.id}\n"
                f"Ism: {admin_data.name}\n"
                f"Account ID: {admin_data.account_id}"
            )

    await safe_state_finish(state)
