from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.group_id import SUPERUSERS


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()
    




class IsSuperUser(BoundFilter):
    key = "is_superuser"

    def __init__(self, is_superuser: bool = True):
        self.is_superuser = is_superuser

    async def check(self, obj: types.Message) -> bool:
        """
        Aiogram requires `check` method (not custom names).
        Works for both messages and callback queries.
        """
        user_id = None
        if isinstance(obj, types.Message):
            user_id = obj.from_user.id
        elif isinstance(obj, types.CallbackQuery):
            user_id = obj.from_user.id

        return (user_id in SUPERUSERS) == self.is_superuser