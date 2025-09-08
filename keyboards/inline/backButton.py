from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callbackData import client_callback

back_keyboard = InlineKeyboardMarkup(
    row_width=1
)

back = InlineKeyboardButton(
    text="⬅️ Ortga", 
    callback_data=client_callback.new(route="back")
)

back_keyboard.insert(back)
