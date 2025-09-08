import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.DriverData import DriverReg

phone_pattern = re.compile(
    r"(?:\+?\d{1,3})?[\s\-]?\(?\d{2,3}\)?[\s\-]?\d{2,3}[\s\-]?\d{2}[\s\-]?\d{2,4}"
)

car_number_pattern = re.compile(
    r"\b([0-9]{2}\s?[A-Z]{1,3}\s?[0-9]{2,3}[A-Z]{0,2}|[A-Z]{1,3}\s?[0-9]{2,3}[A-Z]{0,2})\b",
    re.IGNORECASE
)

NAME_RE = re.compile(r"(?i)\b(ism|name)\s*[:\-]\s*(.+)")

