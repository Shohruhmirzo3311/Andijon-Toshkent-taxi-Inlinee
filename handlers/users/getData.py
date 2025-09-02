from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp
from handlers.users.regexValidation import phone_pattern, car_number_pattern
from states.DriverData import DriverData
from keyboards.inline.callbackData import driver_callback
from filters import IsSuperUser


@dp.callback_query_handler(IsSuperUser(), driver_callback.filter(action="add_driver"))
async def start_add_driver(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer(cache_time=60)
    

    await call.message.answer("Havdovchining ismini kiriting:")
    await DriverData.ism.set()


@dp.message_handler(state=DriverData.ism)
async def get_ism(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("Haydovchining telefon raqamini kiriting:")
    await DriverData.next()


@dp.message_handler(state=DriverData.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone = message.text.strip()

    if not phone_pattern.match(phone):
        await message.answer(
            "❌ Telefon raqam noto‘g‘ri formatda.\n"
            "✅ Masalan: +998901234567 yoki 901234567"
        )
        return
    
    await state.update_data(phone_number=phone)
    await message.answer("Haydovchining mashina raqamini kiriting:")
    await DriverData.next()





@dp.message_handler(state=DriverData.car_number)
async def get_car_number(message: types.Message, state: FSMContext):
    number = message.text.strip().upper()

    if not car_number_pattern.match(number):
        await message.answer(
            "❌ Mashina raqami noto‘g‘ri formatda.\n"
            "✅ Masalan: A123BB yoki AA 123 B"
        )
        return

    await state.update_data(car_number=number)

    # 🔥 Here we save account_id directly (no extra step needed)
    await state.update_data(account_id=message.from_user.id)

    data = await state.get_data()
    ism = data["ism"]
    phone_number = data["phone_number"]
    car_number = data["car_number"]
    account_id = data["account_id"]

    await message.answer(
        f"Haydovchi ma'lumotlari:\n\n"
        f"Ismi: {ism}\n"
        f"Telefon raqami: {phone_number}\n"
        f"Mashina raqami: {car_number}\n"
        f"Account ID: {account_id}"
    )

    await state.finish()
