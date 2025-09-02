from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType





def make_profile_button(user):
    profile_link = f"tg://user?id={user.id}"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        text=f"Mijoz: {user.full_name}",
        url=profile_link
    ))
    return keyboard



