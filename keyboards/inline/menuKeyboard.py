from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callbackData import bot_callback, driver_callback

driver_action_menu = InlineKeyboardMarkup(
    row_width=1
)




driver_list = InlineKeyboardButton("📋 Haydovchilar ro'yxati", callback_data=driver_callback.new(action="driver_list"))
driver_action_menu.insert(driver_list)

add_driver = InlineKeyboardButton("🚗 Haydovchi qo'shish", callback_data=driver_callback.new(action="add_driver"))
driver_action_menu.insert(add_driver)

change_duration = InlineKeyboardButton("⏰ Muddatni uzaytirish", callback_data=driver_callback.new(action="extend_driver"))
driver_action_menu.insert(change_duration)

update_driver = InlineKeyboardButton(text="✍️ Haydovchi ma'lumotlarini tahrirlash", callback_data=driver_callback.new(action="update_driver"))
driver_action_menu.insert(update_driver)

delete_driver = InlineKeyboardButton("🗑️ Haydovchi o'chirish", callback_data=driver_callback.new(action="delete_driver"))
driver_action_menu.insert(delete_driver)



back_button = InlineKeyboardButton(text="⬅️ Orqaga", callback_data="cancel_admin_actions") 
driver_action_menu.insert(back_button)




bot_action_menu = InlineKeyboardMarkup(
    row_width=2
)

view_stats = InlineKeyboardButton(text="📊 Statistika", callback_data=bot_callback.new(action="stats"))
bot_action_menu.insert(view_stats)

bot_action_menu.insert(back_button)


confirm_driver_deletion_keyabord = InlineKeyboardMarkup(row_width=2)


