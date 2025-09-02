from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



from filters import IsPrivate
from keyboards.inline.acceptClient import accept_client_keyboard
from keyboards.inline.callbackData import client_callback
from keyboards.default.CallKeybaord import location, contact
from states.OrderData import OrderForm
from loader import dp, bot
from data.group_id import gr_username



@dp.message_handler(IsPrivate(), lambda msg: "Mijoz" in msg.text)
async def client_menu(message: types.Message):
    await message.answer(
        "Siz Andijon va Toshkent shaharlarida taksi xizmatlaridan foydalanishingiz mumkin.\n\n"
        "Qaysi yo'nalishda buyurtma berasiz?",
        reply_markup=accept_client_keyboard
    )
    



@dp.callback_query_handler(IsPrivate(), client_callback.filter(route=["andijon", "toshkent"]))
async def andijon_tashkent(call: types.CallbackQuery): 
    await call.message.delete()
    await call.answer(cache_time=60)

    await call.message.answer(
        "✍️ Elon berish uchun birzo ma'lumot hamda telefon raqamingizni yuboring..\n\n"
        "Misol: Andijondan Toshkentga soat ... da ketishim kerak...\n yoki: \n"
        "Toshkentdan Andijonga soat  .... da ketishim kerak"

        
    )

    await OrderForm.waiting_for_details.set()




@dp.message_handler(IsPrivate(), state=OrderForm.waiting_for_details)
async def process_order_details(message: types.Message, state: FSMContext):
    await state.update_data(details=message.text)
    
    await message.answer("📍 Iltimos joylashuvingizni yuboring:", reply_markup=location)
    await OrderForm.waiting_for_location.set()






@dp.message_handler(IsPrivate(), content_types=types.ContentTypes.LOCATION, state=OrderForm.waiting_for_location)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=(message.location.latitude, message.location.longitude))

    await message.answer("📞 Endi telefon raqamingizni yuboring:", reply_markup=contact)
    await OrderForm.waiting_for_contact.set()




@dp.message_handler(IsPrivate(), content_types=types.ContentTypes.CONTACT, state=OrderForm.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number)

    data = await state.get_data()
    details = data.get("details")
    location = data.get("location")
    contact = data.get("contact")
    id = message.from_user.id
    full_name = message.from_user.full_name
    profile_link = f"tg://user?id={id}"
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=f"Mijoz: {full_name}", url=profile_link)
    )

    text = (
        f"📝 Buyurtma tafsilotlari:\n\n"
        f"{details}\n\n"
        f"📍 Location: https://maps.google.com/?q={location[0]},{location[1]}\n"
        f"📞 Telefon: {contact}"
        
    )

    # await copy_to_group(bot, text, gr_username)
    await bot.send_message(
        chat_id=gr_username,
        text=text,
        reply_markup=keyboard
    )

    await message.answer(
        "✈️ Buyurtmangiz shofyorlar guruhiga yuborildi!\n"
        "Tez orada siz bilan bog‘lanishadi..."
    )


    try:
        await state.finish()
    except KeyError:
        pass






