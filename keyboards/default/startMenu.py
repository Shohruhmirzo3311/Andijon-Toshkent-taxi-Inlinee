from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

Startmenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚕 Haydovchilar"), 
            KeyboardButton(text="🤖 Bot"),   
        ]
    ],
    resize_keyboard=True
)


roleMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚖 Haydovchi"),   
            KeyboardButton(text="👤 Mijoz"), 
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)