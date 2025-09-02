from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)




contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)