from aiogram.dispatcher.filters.state import State, StatesGroup



class City(StatesGroup):
    name = State()


class CityDel(StatesGroup):
    name = State()


class CityUpdate(StatesGroup):
    name = State()
    new_name = State()