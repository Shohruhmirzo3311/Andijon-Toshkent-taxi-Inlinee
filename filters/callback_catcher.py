from aiogram.dispatcher.filters import Filter
from aiogram import types

from loader import dp

class CallbackActionStartswith(Filter):
    def __init__(self, prefix):
        self.prefix = prefix
    
    async def check(self, call: types.CallbackQuery):
        if not call.data:
            return False
        
        # Parse callback data
        from aiogram.utils.callback_data import CallbackData
        # This is a simplified approach - you might need to adjust based on your callback structure
        return call.data.startswith(self.prefix)

# Register the filter
dp.bind_filter(CallbackActionStartswith)