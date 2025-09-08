from aiogram import types

from keyboards.default.startMenu import Startmenu
from keyboards.inline.callbackData import bot_callback
from keyboards.inline.menuKeyboard import bot_action_menu
from loader import dp


@dp.callback_query_handler(bot_callback.filter(action="about"))
@dp.message_handler(text="about")
async def about_bot(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer(cache_time=60)
    
    about_text = (
        "🤖 *Bot nomi:* Andijon-Toshkent Taxi Bot\n"
        "🚖 *Maqsad:* Ushbu bot Andijon va Toshkent shaharlarida taksi xizmatlarini boshqarish va haydovchilar bilan mijozlar o'rtasidagi aloqani osonlashtirish uchun yaratilgan.\n\n"
        "🔧 *Asosiy funksiyalar:*\n"
        "1. Haydovchilar ro'yxatini boshqarish (qo'shish, tahrirlash, o'chirish)\n"
        "2. Haydovchilarning balansini ko'rish\n"
        "3. Statistika va hisobotlarni ko'rish\n"
        "4. Mijozlar uchun qidiruv va yordam funksiyalari\n\n"
        "📢 *Yangilanishlar:* Bot muntazam ravishda yangilanib boriladi, yangi funksiyalar qo'shiladi va mavjud funksiyalar yaxshilanadi.\n\n"
        "📞 *Aloqa:* Agar sizda savollar yoki takliflar bo'lsa, iltimos, biz bilan bog'laning.\n\n Mirzohid \n\n +9989 94 053 55 50"
    )
    
    await call.message.answer(about_text, parse_mode="Markdown")



@dp.callback_query_handler(bot_callback.filter(action="comments"))
async def feedback(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer(cache_time=60)
    
    await call.message.answer("Aka telefon qiloras... \n\n Shohruhmirzo \n\n +9989 93 754 33 11")



