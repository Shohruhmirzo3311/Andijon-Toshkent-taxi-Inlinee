from aiogram import types
from aiogram.dispatcher import FSMContext



from loader import dp
from filters import IsPrivate
from handlers.users.getData import start_add_driver
from states.DriverData import DriverReg

from keyboards.inline.callbackData import driver_callback
from filters import IsPrivate
from handlers.users.regexValidation import phone_pattern, NAME_RE, car_number_pattern




@dp.message_handler(IsPrivate(), lambda msg: "Haydovchi" in msg.text)
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
    
    account_id = message.from_user.id

    # await db.add_driver(account_id=account_id, name=ism, phone=phone, car_number=car)

    await message.answer(
        "✅ Ro‘yxatdan o‘tish yakunlandi!\n\n"
        f"👤 Ism: {ism}\n"
        f"📞 Telefon: {phone}\n"
        f"🚘 Mashina: {car}\n"
        f"🆔 Account ID: {account_id}"
    )

    await state.finish()
