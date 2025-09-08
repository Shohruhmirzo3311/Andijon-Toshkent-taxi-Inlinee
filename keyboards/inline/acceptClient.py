from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callbackData import client_callback

route_keyboard = InlineKeyboardMarkup(
    row_width=1
)



anjan = InlineKeyboardButton(text="Andijon - Toshkent", callback_data=client_callback.new(route="andijon"))
route_keyboard.insert(anjan)

namangan = InlineKeyboardButton(text="Namangan - Toshkent", callback_data=client_callback.new(route="namangan"))
route_keyboard.insert(namangan)

fargona = InlineKeyboardButton(text="Fargona - Toshkent", callback_data=client_callback.new(route="fargona"))
route_keyboard.insert(fargona)



accept_client_keyboard = InlineKeyboardMarkup(
    row_width=1
)

back_btn = InlineKeyboardButton(
    text="⬅️ Ortga", 
    callback_data=client_callback.new(route="go_back")
)
route_keyboard.insert(back_btn)


andijon_client_keyboard = InlineKeyboardMarkup(
    row_width=1
)



namangan_client_keyboard = InlineKeyboardMarkup(
    row_width=1
)




fargona_client_keyboard = InlineKeyboardMarkup(
    row_width=1
)


#Main cancel
cancel = InlineKeyboardButton(
    text="⬅️ Ortga", 
    callback_data="cancel")



#Andijon
toshkent_anjan = InlineKeyboardButton(
    text="Toshkent - Andijon", callback_data=client_callback.new(route="toshkent_anjan")
)

accept_client_keyboard.insert(toshkent_anjan)
andijon_client_keyboard.insert(toshkent_anjan)


andijon_tashkent = InlineKeyboardButton(
    text="Andijon - Toshkent", callback_data=client_callback.new(route="andijon_tashkent")
)

accept_client_keyboard.insert(andijon_tashkent)
andijon_client_keyboard.insert(andijon_tashkent)




#Namangan
toshkent_namangan = InlineKeyboardButton(
    text="Toshkent - Namangan", callback_data=client_callback.new(route="toshkent_namangan")
)

accept_client_keyboard.insert(toshkent_namangan)
namangan_client_keyboard.insert(toshkent_namangan)

namangan_toshkent = InlineKeyboardButton(
    text="Namangan - Toshkent", callback_data=client_callback.new(route="namangan_toshkent")
)

accept_client_keyboard.insert(namangan_toshkent)
namangan_client_keyboard.insert(namangan_toshkent)



#Fargona
fargona_tashkent = InlineKeyboardButton(
    text="Fag'ona - Toshkent", callback_data=client_callback.new(route="fargona_tashkent")
)

accept_client_keyboard.insert(fargona_tashkent)
fargona_client_keyboard.insert(fargona_tashkent)



toshkent_fargona = InlineKeyboardButton(
    text="Toshkent - Farg'ona", callback_data=client_callback.new(route="toshkent_fargona")
)

accept_client_keyboard.insert(toshkent_fargona)
fargona_client_keyboard.insert(toshkent_fargona)

accept_client_keyboard.insert(cancel)
andijon_client_keyboard.insert(cancel)
namangan_client_keyboard.insert(cancel)
fargona_client_keyboard.insert(cancel)
