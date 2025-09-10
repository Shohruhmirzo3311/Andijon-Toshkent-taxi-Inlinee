from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.group_id import gr_username
from filters import IsPrivate
from keyboards.default.CallKeybaord import contact, location
from keyboards.default.startMenu import roleMenu
from keyboards.inline.acceptClient import (andijon_client_keyboard,
                                           fargona_client_keyboard,
                                           namangan_client_keyboard,
                                           route_keyboard)
from keyboards.inline.backButton import back_keyboard
from keyboards.inline.callbackData import client_callback
from loader import bot, dp
from states.OrderData import OrderForm


@dp.message_handler(lambda msg: "Mijoz" in msg.text)
async def client_menu(message: types.Message):
    await message.answer(
        "Сиз Андижон, Наманган, Фарғона ва Тошкент шаҳарларида такси хизматларидан фойдаланишингиз mumkin.\n\n"
        "Қайси йўналишда буюртма берасиз?",
        reply_markup=route_keyboard
    )




@dp.callback_query_handler(
        IsPrivate(),
        client_callback.filter(route=["andijon", "namangan", "fargona"])
)
async def handle_city_selection(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    await call.answer(cache_time=60)
    
    city = callback_data['route']
    text=f"{city.title()} шаҳри танланди. Энди йўналишни танланг",
    
    if city == "andijon":
        keyboard = andijon_client_keyboard
    elif city == "namangan":
        keyboard = namangan_client_keyboard
    elif city == "fargona":
        keyboard = fargona_client_keyboard
    
    else:
        return    
    
    await call.message.answer(text, reply_markup=keyboard)



@dp.callback_query_handler( client_callback.filter(route=[
    "toshkent_anjan", "andijon_tashkent", "toshkent_namangan", 
    "namangan_toshkent", "fargona_tashkent", "toshkent_fargona"
]))
async def handle_route_selection(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    await call.answer(cache_time=60)

    await call.message.answer(
        "✍️ Элон бериш учун бирзо маълумот ҳамда телефон рақамингизни юборинг..\n\n"
        "Мисол: Андижондан Тошкентга соат ... да кетишим керак...\n ёки: \n"
        "Тошкентдан Андижонга соат  .... да кетишим керак",
        
        reply_markup=back_keyboard

        
    )

    await OrderForm.waiting_for_details.set()




@dp.message_handler(state=OrderForm.waiting_for_details)
async def process_order_details(message: types.Message, state: FSMContext):
    await state.update_data(details=message.text)
    
    await message.answer("📍 Илтимос жойлашувингизни юборинг:", reply_markup=location)
    await OrderForm.waiting_for_location.set()






@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=OrderForm.waiting_for_location)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=(message.location.latitude, message.location.longitude))

    await message.answer("📞 Энди телефон рақамингизни юборинг:", reply_markup=contact)
    await OrderForm.waiting_for_contact.set()




@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=OrderForm.waiting_for_contact)
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
        "📤 Буюртмангиз шофёрлар гуруҳига юборилди!\n"
        "Тез орада сиз билан боғланишади..."
    )


    try:
        await state.finish()
    except KeyError:
        pass







# Back handler (for all ReplyKeyboard steps)
@dp.message_handler(Text(equals="⬅️ Orqaga"), state="*")
async def reply_back_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == OrderForm.waiting_for_location.state:
        # back to details step
        await OrderForm.waiting_for_details.set()
        await message.answer("✍️ Буюртма ҳақида маълумотни қайта киритинг:")

    elif current_state == OrderForm.waiting_for_contact.state:
        # back to location step
        await OrderForm.waiting_for_location.set()
        await message.answer("📍 Жойлашувингизни қайта юборинг:", reply_markup=location)

    else:
        # fallback → go to main menu
        await state.finish()
        await message.answer("🏠 Asosiy menyuga qaytdingiz", reply_markup=roleMenu)
