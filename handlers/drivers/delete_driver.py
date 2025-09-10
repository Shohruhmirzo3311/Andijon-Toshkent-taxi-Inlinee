from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.sql import select

import utils.db_api.driverDb as db
import utils.db_api.init_tables as sas
from filters import IsSuperUser
from handlers.users.regexValidation import car_number_pattern
from keyboards.inline.callbackData import driver_callback
from keyboards.inline.menuKeyboard import driver_action_menu
from loader import dp
from states.DriverData import DeleteDriver
from states.state_finish import safe_state_finish


@dp.callback_query_handler(IsSuperUser(), driver_callback.filter(action="delete_driver"))
async def start_delete_driver(call: types.CallbackQuery):
    """Ask for car number to delete driver"""
    await call.message.delete()
    await call.answer()

    await call.message.answer(
        "🗑️ Haydovchini o'chirish\n\n"
        "🚗 O'chirish uchun mashina raqamini kiriting:"
    )
    await DeleteDriver.waiting_for_car_number.set()


@dp.message_handler(state=DeleteDriver.waiting_for_car_number)
async def process_delete_driver(message: types.Message, state: FSMContext):
    car_number = message.text.strip().upper()

    if not car_number_pattern.match(car_number):
        await message.answer(
            "❌ Mashina raqami noto'g'ri formatda.\n"
            "✅ Masalan: A123BB yoki AA 123 B\n\n"
            "🚗 Iltimos, qaytadan kiriting:"
        )
        return

    async with sas.AsyncSessionLocal() as session:
        result = await session.execute(
            select(db.Driver).where(db.Driver.car_number == car_number)
        )
        driver = result.scalar()

    if not driver:
        await message.answer(
            f"❌ {car_number} raqamli haydovchi topilmadi.\n\n"
            "Boshqa mashina raqamini kiriting yoki /cancel buyrug'i bilan bekor qiling:"
        )
        return

    await state.update_data(car_number=car_number)

    await message.answer(
        f"🔴 Quyidagi haydovchini o'chirishni tasdiqlaysizmi?\n\n"
        f"👤 Ismi: {driver.name}\n"
        f"📞 Telefon: {driver.phone}\n"
        f"🚗 Mashina: {driver.car_number}\n"
        f"📂 Toifa: {driver.type}\n\n"
        f"⚠️ Bu amalni qaytarib bo'lmaydi!\n\n"
        f"👉 Tasdiqlash uchun: /confirm_delete\n"
        f"👉 Bekor qilish uchun: /cancel_delete"
    )
    await DeleteDriver.confirmation.set()


@dp.message_handler(commands=["confirm_delete"], state=DeleteDriver.confirmation)
async def confirm_delete_driver(message: types.Message, state: FSMContext):
    data = await state.get_data()
    car_number = data.get("car_number")
    name = data.get("name")

    async with sas.AsyncSessionLocal() as session:
        deleted = await db.delete_driver_by_car_number(session, car_number)

    if deleted:
        await message.answer(
            f"✅ Haydovchi muvaffaqiyatli o'chirildi!\n\n🚗 \n\n {car_number}"
        )
    else:
        await message.answer("❌ Haydovchini o'chirishda xatolik yuz berdi.")

    await safe_state_finish(state)


@dp.message_handler(commands=["cancel_delete"], state=DeleteDriver.confirmation)
async def cancel_delete_driver(message: types.Message, state: FSMContext):
    await message.answer(
        "❌ Haydovchini o'chirish bekor qilindi.\n\n"
        "Boshqa amalni bajarish uchun menyudan tanlang.",
        reply_markup=driver_action_menu
    )
    await safe_state_finish(state)
