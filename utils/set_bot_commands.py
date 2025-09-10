from aiogram import types
from utils.db_api.admin_data import laod_admins

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
        ]
    )
    


async def set_default_commands(dp):
    admin_list = await laod_admins()
    
    for admin_id in admin_list:
        if admin_id:
    
            await dp.bot.set_my_commands(
                [
                    types.BotCommand("start", "Botni ishga tushurish"),            
                    types.BotCommand("add_admin", "Admin qo'shish"),
                    types.BotCommand("delete_admin", "Admin o'chirish"),
                    types.BotCommand("admins", "Adminlar ro'yxati"),
                    types.BotCommand("add_city", "Shahar qo'shish"),
                    types.BotCommand("cities", "Shaharlar ro'yxati"),  
                    types.BotCommand("delete_city", "Shahar ocirish"), 
                    types.BotCommand("update_city", "Shahar nomini o'zgartirish"),           
                ]
            )
        else:
            return