from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)
        ],
        [
            KeyboardButton(text="⬅️ Orqaga")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)





contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True),
            KeyboardButton(text="⬅️ Orqaga"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)