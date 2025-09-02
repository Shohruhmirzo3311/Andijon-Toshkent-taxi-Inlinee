from aiogram import types
from loader import dp

@dp.inline_handler(text=["toshkent", "andijon"])
async def route_query(query: types.InlineQuery):
    await query.answer(
        results=[
            types.InlineQueryResult
        ]
    )