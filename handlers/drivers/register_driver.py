from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.exc import IntegrityError

import utils.db_api.driverDb as db
import utils.db_api.init_tables as sas
from filters import IsSuperUser
from handlers.users.regexValidation import car_number_pattern, phone_pattern
from keyboards.inline.callbackData import driver_callback
from loader import dp
from states.DriverData import DriverData
from states.state_finish import safe_state_finish


@dp.callback_query_handler(IsSuperUser(), driver_callback.filter(action="add_driver"))
async def start_add_driver(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer(cache_time=60)
    await call.message.answer("Haydovchining ismini kiriting:")
    await DriverData.ism.set()

@dp.message_handler(state=DriverData.ism)
async def get_ism(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("Haydovchining telefon raqamini kiriting:")
    await DriverData.phone.set()

@dp.message_handler(state=DriverData.phone)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone = message.text.strip()

    if not phone_pattern.match(phone):
        await message.answer(
            "❌ Telefon raqam noto'g'ri formatda.\n"
            "✅ Masalan: +998901234567 yoki 901234567"
        )
        return
    
    await state.update_data(phone=phone)
    await message.answer("Haydovchining mashina raqamini kiriting:")
    await DriverData.car.set()

@dp.message_handler(state=DriverData.car)
async def get_car_number(message: types.Message, state: FSMContext):
    number = message.text.strip().upper()

    if not car_number_pattern.match(number):
        await message.answer(
            "❌ Mashina raqami noto'g'ri formatda.\n"
            "✅ Masalan: A123BB yoki AA 123 B"
        )
        return

    await state.update_data(car=number)
    await message.answer("Haydovchining Account ID sini kiriting:")
    await DriverData.account_id.set()

@dp.message_handler(state=DriverData.account_id)
async def get_account_id(message: types.Message, state: FSMContext):
    account_id = message.text.strip()
    
    # Validate account ID is a number
    if not account_id.isdigit():
        await message.answer("❌ Account ID faqat raqamlardan iborat bo'lishi kerak. Iltimos, qayta kiriting:")
        return
    
    await state.update_data(account_id=account_id)
    await message.answer("Haydovchi necha kunga aktiv bo'lsin? (Kunlar sonini kiriting):")
    await DriverData.active_until.set()

@dp.message_handler(state=DriverData.active_until)
async def get_active_days(message: types.Message, state: FSMContext):
    try:
        days = int(message.text.strip())
        if days <= 0:
            await message.answer("❌ Iltimos, 0 dan katta raqam kiriting:")
            return
            
        # Calculate active_until date
        active_until = datetime.now() + timedelta(days=days)
        await state.update_data(active_until=active_until)
        
        # Ask for category
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("🚘 Oddiy", callback_data="driver_category:oddiy"),
            InlineKeyboardButton("✨ Comfort", callback_data="driver_category:comfort")
        )

        data = await state.get_data()
        ism = data.get("ism", "Noma'lum")
        phone = data.get("phone", "Noma'lum")
        car = data.get("car", "Noma'lum")
        account_id = data.get("account_id", "Noma'lum")
        active_until = data.get("active_until", "Noma'lum")
        
        await message.answer(
            f"Haydovchi ma'lumotlari:\n\n"
            f"👤 Ismi: {ism}\n"
            f"📞 Telefon: {phone}\n"
            f"🚘 Mashina: {car}\n"
            f"🆔 Account ID: {account_id}\n"
            f"⏰ Faoliyat muddati: {active_until.strftime('%Y-%m-%d %H:%M')}\n\n"
            "👉 Toifani tanlang:",
            reply_markup=keyboard
        )
        
        await DriverData.category.set()
        
    except ValueError:
        await message.answer("❌ Iltimos, faqat raqam kiriting (masalan: 30):")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('driver_category:'), state=DriverData.category)
async def select_category(call: types.CallbackQuery, state: FSMContext):
    try:
        category = call.data.split(":")[1]
        data = await state.get_data()
        
        ism = data.get("ism", "Noma'lum")
        phone = data.get("phone", "Noma'lum")
        car = data.get("car", "Noma'lum")
        account_id = data.get("account_id", "Noma'lum")
        active_until = data.get("active_until", "Noma'lum")

        async with sas.AsyncSessionLocal() as session:
            success, msg, driver_id = await db.add_driver(
                session,
                account_id=int(account_id),
                name=ism,
                phone=phone,
                car_number=car,
                category=category,
                active_until=active_until
            )
            
            if success:
                await call.message.edit_text(
                    f"✅ Ro'yxatdan o'tish admin tasdiqlashiga yuborildi!\n\n"
                    f"{msg}\n"
                    f"👤 Ism: {ism}\n"
                    f"📞 Telefon: {phone}\n"
                    f"🚘 Mashina: {car}\n"
                    f"🆔 Account ID: {account_id}\n"
                    f"📂 Toifa: {category.capitalize()}\n"
                    f"⏰ Faoliyat muddati: {active_until.strftime('%Y-%m-%d %H:%M')}"
                )
                await safe_state_finish(state)
            else:
                await call.message.answer(msg)
                # Don't finish state to allow re-entry
                
    except IntegrityError as e:
        await call.message.answer("❌ Bu haydovchi allaqachon ro'yxatdan o'tkazilgan. Iltimos, boshqa ma'lumotlar kiriting.")
        await safe_state_finish(state)
    except ValueError as e:
        await call.message.answer("❌ Account ID noto'g'ri formatda. Iltimos, boshqatdan urunib ko'ring.")
    except Exception as e:
        print(f"Database error: {str(e)}")
        await call.message.answer("❌ Ma'lumotlar bazasiga qo'shishda xatolik yuz berdi. Iltimos, keyinroq qayta urunib ko'ring yoki administratorga murojaat qiling.")
        await safe_state_finish(state)
    
    await call.answer()

