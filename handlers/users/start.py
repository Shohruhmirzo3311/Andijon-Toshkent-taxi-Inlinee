from aiogram import filters, types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.group_id import SUPERUSERS
from filters import IsGroup, IsPrivate, IsSuperUser
from keyboards.default.startMenu import Startmenu, roleMenu
from loader import dp
from utils.db_api.admin_data import ADMINS, laod_admins





@dp.message_handler(IsPrivate(), IsSuperUser(), commands=['start'])
async def admin_start(msg: types.Message):
    await msg.answer('Xush kelibsiz, Admin!', reply_markup=Startmenu)




@dp.message_handler(IsPrivate(), CommandStart())
async def user_start(message: types.Message):
    admins_list = await laod_admins()
    
    if message.from_user.id in admins_list:
        return

    await message.answer(f"Salom, {message.from_user.full_name}!")
    await message.answer("Tanlang:", reply_markup=roleMenu)




@dp.message_handler(IsGroup(), CommandStart())
async def group_start(message: types.Message):
    admins_list = await laod_admins()
    
    if message.from_user.id in admins_list:
        return
    await message.answer(f"Salom, {message.from_user.full_name}\n\n Guruhga xush kelibsiz!")
    

