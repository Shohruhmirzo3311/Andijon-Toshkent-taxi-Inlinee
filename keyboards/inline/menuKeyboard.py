from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callbackData import driver_callback, bot_callback



driver_action_menu = InlineKeyboardMarkup(
    row_width=1
)


driver_list = InlineKeyboardButton(text="🚕 Haydovchilar ro'yxati", callback_data=driver_callback.new(action="driver_list"))
driver_action_menu.insert(driver_list)

add_driver = InlineKeyboardButton(text="➕ Haydovchi qo'shish", callback_data=driver_callback.new(action="add_driver")) 
driver_action_menu.insert(add_driver)

get_driver_balance = InlineKeyboardButton(text="💰 Haydovchi balansini ko'rish", callback_data=driver_callback.new(action="balance"))
driver_action_menu.insert(get_driver_balance)

update_driver = InlineKeyboardButton(text="✍️ Haydovchi ma'lumotlarini tahrirlash", callback_data=driver_callback.new(action="update_driver"))
driver_action_menu.insert(update_driver)

delete_driver = InlineKeyboardButton(text="❌ Haydovchini o'chirish", callback_data=driver_callback.new(action="delete_driver"))
driver_action_menu.insert(delete_driver)



back_button = InlineKeyboardButton(text="⬅️ Orqaga", callback_data="cancel") 
driver_action_menu.insert(back_button)




bot_action_menu = InlineKeyboardMarkup(
    row_width=2
)

view_stats = InlineKeyboardButton(text="📊 Statistika", callback_data=bot_callback.new(action="stats"))
bot_action_menu.insert(view_stats)

lookup = InlineKeyboardButton(text="🔍 Qidirish", switch_inline_query_current_chat="")
bot_action_menu.insert(lookup)



help_button = InlineKeyboardButton(text="🆘 Yordam", callback_data=bot_callback.new(action="help"))
bot_action_menu.insert(help_button)

comments = InlineKeyboardButton(text="💬 Fikr-mulohaza", callback_data=bot_callback.new(action="comments"))
bot_action_menu.insert(comments)

about = InlineKeyboardButton(text="ℹ️ Bot haqida", callback_data=bot_callback.new(action="about"))
bot_action_menu.insert(about)

bot_action_menu.insert(back_button)