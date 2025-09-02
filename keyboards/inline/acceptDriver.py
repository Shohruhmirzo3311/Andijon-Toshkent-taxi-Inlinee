from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

worker_task_menu = InlineKeyboardMarkup(row_width=1)

contact = InlineKeyboardButton(
    text="📞 Murojaat qilish\n\n Telefon: 95 053 55 50",

    url="https://t.me/shox3311"   
)

worker_task_menu.add(contact)


