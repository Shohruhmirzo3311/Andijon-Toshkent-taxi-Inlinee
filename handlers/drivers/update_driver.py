from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.sql import select

import utils.db_api.driverDb as db
import utils.db_api.init_tables as sas
from filters import IsSuperUser
from handlers.users.regexValidation import phone_pattern
from keyboards.inline.callbackData import driver_callback
from keyboards.inline.menuKeyboard import driver_action_menu
from loader import dp
from states.DriverData import UpdateDriver
from states.state_finish import safe_state_finish


@dp.callback_query_handler(IsSuperUser, driver_callback.filter(action="update_driver"))
async def update_driver(call: CallbackQuery):
    await call.message.delete()
    await call.answer()
    await call.message.answer("✍️ Haydovchining telefon raqamini kiriting:")
    await UpdateDriver.form.set()

    


@dp.message_handler(state=UpdateDriver.form)
async def update_driver_data(message: Message, state: FSMContext):
    phone = message.text.strip()
    
    if not phone_pattern.match(phone):
        await message.answer("Telefon raqamini togri formatda kiriting..\n"
                             "Masalan: +998 90 123 45 67")
        return 
    
    
    async with sas.AsyncSessionLocal() as session:
        result = await session.execute(
            select(db.Driver).where(db.Driver.phone == phone)
        )
        driver = result.scalar()

    if not driver:
        await message.answer(
            f"❌ {phone} raqamli haydovchi topilmadi.\n\n"
            "Boshqa mashina raqamini kiriting yoki /cancel buyrug'i bilan bekor qiling:"
        )
        return

    await state.update_data(
        driver_phone=driver.phone,
        driver_name=driver.name,
        driver_car_number=driver.car_number,
        driver_type=driver.type,
        driver_active_until=driver.active_until,
        driver_is_active=driver.is_active
    )
    
    
    if message.text == "/cancel":
        await safe_state_finish(state)
    
    await message.answer(
        f"🔴 Quyidagi haydovchini malumotlarini tahrirlashingiz mumkin\n\n"
        f"👤 Ismi: {driver.name}\n"
        f"📞 Telefon: {driver.phone}\n"
        f"🚗 Mashina: {driver.car_number}\n"
        f"📂 Toifa: {driver.type}\n\n"
        f"⏰ Faollik muddati: {driver.active_until}\n"
        f"🔁 Active yoki toxtagan: {driver.is_active}" 
        f"⚠️ Bu amalni qaytarib bo'lmaydi!\n\n"
        "👉 Yangi ma'lumotlarni kiriting. Masalan: yangi ism, yangi mashina raqami. Agar o'zgartirish kerak bo'lmasa, **skip** deb yozing.\n"
        "👉 O'zgarishlarni bekor qilish uchun **/cancel** buyrug'ini kiriting."
    )
    await UpdateDriver.waiting_for_new_data.set()
    


from datetime import datetime


@dp.message_handler(state=UpdateDriver.waiting_for_new_data)
async def process_new_data_and_update(message: Message, state: FSMContext):
    new_data_input = message.text.strip()

    if new_data_input.lower() == "/cancel":
        await message.answer("❌ Haydovchi ma'lumotlarini tahrirlash bekor qilindi.")
        await safe_state_finish(state)
        return

    # Old data
    data = await state.get_data()
    original_phone = data.get("driver_phone")

    # Parse user input
    new_values = {}
    # Support both newline-separated and semicolon-separated input
    parts = [p.strip() for p in new_data_input.replace(";", "\n").split("\n") if p.strip()]

    for part in parts:
        if ":" not in part:
            continue
        key, value = [x.strip() for x in part.split(":", 1)]

        if key.lower() in ["ism", "ismi"]:
            new_values["name"] = value
        elif key.lower() in ["telefon", "phone"]:
            new_values["phone"] = value
        elif key.lower() in ["mashina", "car", "car_number"]:
            new_values["car_number"] = value
        elif key.lower() in ["toifa", "type"]:
            new_values["type"] = value
        elif key.lower() in ["is_active", "status"]:
            new_values["is_active"] = value.lower() in ["true", "1", "ha", "yes"]
        elif key.lower() in ["active_until", "muddat", "faollik_muddati"]:
            try:
                new_values["active_until"] = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                await message.answer("❌ Sana formati noto'g'ri. Masalan: 2025-12-31")
                return


    if not new_values:
        await message.answer("⚠️ Yangi qiymatlar topilmadi. Hech narsa o‘zgartirilmadi.")
        await safe_state_finish(state)
        return

    async with sas.AsyncSessionLocal() as session:
        updated_driver = await db.update_driver_by_phone_number(session, original_phone, new_values)

    if updated_driver:
        await message.answer(
            f"✅ Haydovchi ma'lumotlari yangilandi!\n\n"
            f"👤 {updated_driver.name}\n"
            f"📞 {updated_driver.phone}\n"
            f"🚗 {updated_driver.car_number}\n"
            f"📂 {updated_driver.type}\n"
            f"⏰ {updated_driver.active_until}\n"
            f"🔁 {updated_driver.is_active}"
        )
    else:
        await message.answer("❌ Yangilashda xatolik yuz berdi.")

    await safe_state_finish(state)




@dp.message_handler(commands=["confirm_update"], state=UpdateDriver.second)
async def confirm_update_driver(message: Message, state: FSMContext):
    data = await state.get_data()
    phone = data.get("phone")

    async with db.AsyncSessionLocal() as session:
        updated = await db.update_driver_by_phone_number(session, phone)

    if updated:
        await message.answer(
            f"✅ Haydovchi muvaffaqiyatli tahrirlandi!\n\n🚗 \n\n {phone}"
        )
    else:
        await message.answer("❌ Haydovchi malumootlarini tahrirlashda  xatolik yuz berdi.")

    await safe_state_finish(state)


@dp.message_handler(commands=["cancel_update"], state=UpdateDriver.second)
async def cancel_update_driver(message: Message, state: FSMContext):
    await message.answer(
        "❌ Haydovchi malumotlarini tahrirlash bekor qilindi.\n\n"
        "Boshqa amalni bajarish uchun menyudan tanlang.",
        reply_markup=driver_action_menu
    )
    await safe_state_finish(state)
