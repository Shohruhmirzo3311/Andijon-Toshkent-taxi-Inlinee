from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

import data.driverDb as db  # Your DB module
import data.init_tables as ses
from data.group_id import SUPERUSERS
from filters import IsPrivate, IsSuperUser
from handlers.users.regexValidation import (NAME_RE, car_number_pattern,
                                            phone_pattern)
from loader import dp
from states.DriverData import AdminApprove, DriverReg
from keyboards.inline.acceptDriver import driver_status
from keyboards.inline.callbackData import admin_driver_callback
from keyboards.inline.acceptDriver import admin_keyboard


@dp.message_handler(IsPrivate(), lambda msg: "🚖 Haydovch" in msg.text)
async def driver_become(message: types.Message):
    await message.answer(
        "✍️ Iltimos, bitta xabarda haydovchi ma’lumotlarini yuboring.\n\n"
        "Format (istalgan tartibda, har biri yangi qatorda bo‘lishi mumkin):\n"
        "• Ism (ixtiyoriy, aks holda Telegram ismingiz olinadi)\n"
        "• Telefon: +998901234567 yoki 901234567 (Telegram acccountniki bolishi shart)\n"
        "• Mashina: A123BB yoki AA 123 B\n\n"
        "Misol:\n"
        "Ism: Shohruhmirzo\n"
        "Telefon: +998 90 123 45 67\n"
        "Mashina: 01 A123BC"
    )
    await DriverReg.form.set()



def extract_name(text: str, fallback: str) -> str:
    m = NAME_RE.search(text)
    return m.group(2).strip() if m else fallback



def extract_phone(text: str, fallback: str = "") -> str:
    clean = text.replace(" ", "").replace("-", "")
    m = phone_pattern.search(text) or phone_pattern.search(clean)
    return m.group(0).strip() if m else fallback



def extract_car(text: str, fallback: str = "") -> str:
    m = car_number_pattern.search(text.upper())
    return m.group(0).strip() if m else fallback



@dp.message_handler(state=DriverReg.form, content_types=types.ContentTypes.TEXT)
async def driver_form_handler(message: types.Message, state: FSMContext):
    text = message.text

    ism = extract_name(text, fallback=message.from_user.full_name)
    phone = extract_phone(text, fallback=message.from_user.username or "")
    car = extract_car(text)

    errors = []
    if not phone:
        errors.append("📞 Telefon raqami topilmadi yoki format noto‘g‘ri.\n"
                      "Masalan: +998901234567 yoki 901234567")
    if not car:
        errors.append("🚘 Mashina raqami topilmadi yoki format noto‘g‘ri.\n"
                      "Masalan: A123BB yoki AA 123 B")

    if errors:
        await message.answer("❌ Xatolik:\n\n" + "\n\n".join(errors) +
                             "\n\nIltimos, ma’lumotlarni bitta xabarda to‘g‘ri yuboring.")
        return
    
    # Store data in state for callback to use
    await state.update_data(ism=ism, phone=phone, car=car, account_id=message.from_user.id)
    
    # Send category selection keyboard (state remains active)
    
    
    await message.answer("Toifani tanlang:", reply_markup=driver_status)



@dp.callback_query_handler(lambda c: c.data.startswith('category:'), state=DriverReg.form)
async def select_category(call: types.CallbackQuery, state: FSMContext):
    category = call.data.split(':')[1]
    
    data = await state.get_data()
    ism = data.get("ism")
    phone = data.get("phone")
    car = data.get("car")
    account_id = data.get("account_id")
    
    async with ses.AsyncSessionLocal() as session:
        success, msg, driver_id = await db.add_driver(
            session, 
            account_id=account_id, 
            name=ism, 
            phone=phone, 
            car_number=car, 
            category=category,
            active_until=None,
        )
    
    if success:
        await call.message.edit_text(
            f"✅ Ro‘yxatdan o‘tish admin tasdiqlashiga yuborildi!\n\n"
            f"{msg}\n"
            f"👤 Ism: {ism}\n"
            f"📞 Telefon: {phone}\n"
            f"🚘 Mashina: {car}\n"
            f"🆔 Account ID: {account_id}\n"
            f"📂 Toifa: {category.capitalize()}"
        )

        # send to admin
        info_text = (
            "Yangi haydovchi tasdiqlash kerak:\n\n"
            f"👤 Ism: {ism}\n"
            f"📞 Telefon: {phone}\n"
            f"🚘 Mashina: {car}\n"
            f"🆔 Account ID: {account_id}\n"
            f"📂 Toifa: {category.capitalize()}"
        )
        admin_keyboard.add(
            InlineKeyboardButton("Tasdiqlash", callback_data=admin_driver_callback.new(a="ok", id=driver_id))
        )
        admin_keyboard.add(
            InlineKeyboardButton("Bekor qilish", callback_data=admin_driver_callback.new(a="no", id=driver_id))
        )

        await dp.bot.send_message(SUPERUSERS, info_text, reply_markup=admin_keyboard)

        # ✅ only reset state if success
        await state.finish()

    else:
        # ❌ show error and ask again (keep FSM active!)
        await call.message.answer(
            msg + "\n\n✍️ Iltimos, qayta urining.\n"
            "Format:\n"
            "Ism: Shohruhmirzo\n"
            "Telefon: +998901234567\n"
            "Mashina: 01A123BC"
        )

    # Always answer callback so button doesn’t freeze
    await call.answer()




@dp.callback_query_handler(IsSuperUser(), admin_driver_callback.filter())
async def admin_driver_action(call: types.CallbackQuery, callback_data: dict):
    action = call["a"]
    driver_id = int(callback_data["id"])
    
    async with ses.AsyncSessionLocal() as session:
        driver = await db.get_driver_by_id(session, driver_id)
        if not driver:
            await call.answer("Haydovchi topilmadi!", show_alert=True)
            return
        
        if action == "cancel":
            async with ses.AsyncSessionLocal() as session:
                deleted = await db.delete_driver(session, driver_id)
            if deleted:
                await dp.bot.send_message(driver.account_id, "❌ Ro‘yxatdan o‘tish rad etildi.")
                await call.message.edit_text(call.message.text + "\n\nBekor qilindi.")
                await call.answer("Bekor qilindi")
            else: 
                await call.answer("Xato: O'chirib bo'lmadi", show_alert=True)
                
        elif action == "accept":
            await AdminApprove.days.set()
            state = FSMContext(storage=dp.storage, chat=call.message.chat.id, user=call.from_user.id)
            await state.update_data(driver_id=driver_id)
            await call.message.edit_text(call.message.text + "\n\nFaollik muddatini kunlarda kiriting:")
            await call.answer("Kunlarni kiriting.")


@dp.message_handler(state=AdminApprove.days, content_types=types.ContentType.TEXT)
async def set_days(message: types.Message, state: FSMContext):
    try:
        days = int(message.text.strip())
        if days <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Notogri son. Butun son kiriting")
        return
    
    data = await state.get_data()
    driver_id = data.get("driver_id")
    
    async with ses.AsyncSessionLocal() as session:
        success = await db.set_active_until(session, driver_id, days)
        driver = await db.get_driver_by_id(session, driver_id)
    
    if success:
        await dp.bot.send_message(driver.account_id,
                                  f"Ro'yxatdan o'tish tasdiqlaandi!\nFaollik: {days} kun.\nAdmin bilan bog'lanish: '@shox3311'")
        
        await message.answer(
            f"Haydovchi {days} kunlik faollashtirildi." 
        )
    else: 
        await message.answer("Xato: Yangilash bo'lmadi.")
    
    await state.finish()
    



