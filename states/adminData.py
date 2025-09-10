from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminData(StatesGroup):
    name = State()
    account_id = State()
    

class AdminDeletion(StatesGroup):
    form = State()
    
class AdminUpdate(StatesGroup):
    get_name = State()
    new_name = State()
