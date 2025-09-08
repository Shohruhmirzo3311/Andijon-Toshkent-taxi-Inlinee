from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


worker_task_menu = InlineKeyboardMarkup(row_width=1)

contact = InlineKeyboardButton(
    text="📞 Murojaat qilish\n\n Telefon: 95 053 55 50",

    url="https://t.me/shox3311"   
)

worker_task_menu.add(contact)


driver_status = InlineKeyboardMarkup(row_width=2)
driver_status.add(InlineKeyboardButton("Comfort", callback_data="category:comfort"))
driver_status.add(InlineKeyboardButton("Oddiy", callback_data="category:oddiy"))
    
    


admin_keyboard = InlineKeyboardMarkup(row_width=2)
