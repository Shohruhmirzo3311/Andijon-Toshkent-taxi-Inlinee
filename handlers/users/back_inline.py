from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters import IsPrivate
from keyboards.default.startMenu import Startmenu, roleMenu
from keyboards.inline.acceptClient import route_keyboard
from keyboards.inline.callbackData import client_callback
from loader import dp


#Back to main role menu
@dp.callback_query_handler(IsPrivate(), client_callback.filter(route='go_back'))
async def go_back_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Asosiy menuga qaytdingiz 👇",
        
        reply_markup=roleMenu
    )
    await callback.answer()



# Back to city keyboard Andijon / Toshkent / Fargona --------> this is the first one 
@dp.callback_query_handler(IsPrivate(), Text(equals="cancel"))
async def cancel_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Ortga qaytish",
        reply_markup=route_keyboard
    )
    await callback.answer()



#Back to route keyboard
@dp.callback_query_handler(client_callback.filter(route="back"), state="*")
async def back_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        if await state.get_state() is not None:
            await state.reset_state(with_data=False)
    except KeyError:
        # user had no state stored, safe to ignore
        pass

    await call.message.delete()
    await call.message.answer(
        "Yo'nalishni tanlang",
        reply_markup=route_keyboard
    )



#Back in admin actions in admin part of the bot

@dp.callback_query_handler(IsPrivate(), Text(equals="cancel_admin_actions"))
async def cancel_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Asosiy menuga qaytdingiz 👇",        
        reply_markup=Startmenu
    )
    await callback.answer()
