from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

# class IsPrivate(BoundFilter):
#     async def check(self, message: types.Message):
#         return message.chat.type == types.ChatType.PRIVATE
    


class IsPrivate(BoundFilter):
    async def check(self, obj):
        if isinstance(obj, types.Message):
            return obj.chat.type == types.ChatType.PRIVATE
        elif isinstance(obj, types.CallbackQuery):
            return obj.message.chat.type == types.ChatType.PRIVATE
        return False
