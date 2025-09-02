from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callbackData import client_callback

accept_client_keyboard = InlineKeyboardMarkup(
    row_width=2
)

toshkent = InlineKeyboardButton(
    text="🚖 Toshkentdan Andijonga", callback_data=client_callback.new(route="toshkent")
)

accept_client_keyboard.insert(toshkent)

andijon = InlineKeyboardButton(
    text="🚖 Andijondan Toshkentga", callback_data=client_callback.new("andijon")
)

accept_client_keyboard.insert(andijon)


