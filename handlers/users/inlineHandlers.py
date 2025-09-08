from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.acceptClient import accept_client_keyboard
from keyboards.inline.callbackData import client_callback
from loader import dp


@dp.inline_handler()
async def inline_start(query: types.InlineQuery):
    results = []

    # ✅ If user typed only @BotName (no query text)
    if not query.query.strip():
        results.append(
            types.InlineQueryResultArticle(
                id="start_bot",
                title="🚖 Водий такси хизматлари",
                description="Андижон / Наманган / Фарғона ↔ Тошкент",
                input_message_content=types.InputTextMessageContent(
                    message_text="🚖 Водий такси"
                ),
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="🚖 Такси хизматини бошлаш",
                        url="https://t.me/toshkent_t_bot?start=start_inline"
                    )
                )
            )
        )
    else:
        # ❌ If they typed something → ignore or show a simple "no result"
        results.append(
            types.InlineQueryResultArticle(
                id="not_used",
                title="❌ Фақат @toshkent_t_bot ёзинг",
                description="Қидирув шарт эмас",
                input_message_content=types.InputTextMessageContent(
                    message_text="❌ Нотўғри қидирув"
                )
            )
        )

    await query.answer(results=results, cache_time=1)
