from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import filters



from loader import dp
from filters import IsPrivate, IsGroup
from keyboards.default.startMenu import Startmenu, roleMenu
from data.group_id import SUPERUSERS





@dp.message_handler(IsPrivate(), filters.IDFilter(chat_id=SUPERUSERS), commands=['start'])
async def admin_start(msg: types.Message):
    await msg.answer('Xush kelibsiz, Admin!', reply_markup=Startmenu)




@dp.message_handler(IsPrivate(), CommandStart())
async def user_start(message: types.Message):
    if message.from_user.id in SUPERUSERS:
        return
    await message.answer(f"Salom, {message.from_user.full_name}!")
    await message.answer("Tanlang:", reply_markup=roleMenu)




@dp.message_handler(IsGroup(), CommandStart())
async def group_start(message: types.Message):
    if message.from_user.id in SUPERUSERS:
        return
    await message.answer(f"Salom, {message.from_user.full_name}\n\n Guruhga xush kelibsiz!")
    