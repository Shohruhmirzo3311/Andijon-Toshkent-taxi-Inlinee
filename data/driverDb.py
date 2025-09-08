from datetime import datetime, timedelta, timezone

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, select, update
from typing import Optional

from data.init_tables import Base


class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    car_number = Column(String, nullable=False, unique=True)
    active_until = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False)
    type = Column(String, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'driver'  # Base identity
    }
    
class ComfortDriver(Driver):
    __mapper_args__ = {
        'polymorphic_identity': 'comfort'
    }

class OddiyDriver(Driver):
    __mapper_args__ = {
        'polymorphic_identity': 'oddiy'
    }
    

async def add_driver(
    session: AsyncSession, 
    account_id: int, 
    name: str, 
    phone: str, 
    car_number: str, 
    category: str,
    active_until:datetime,
):
    """
    Add a new driver if not exists.
    Returns (success: bool, message: str, driver_id: Optional[int]).
    """
    stmt = select(Driver).where(
        (Driver.phone == phone) | (Driver.car_number == car_number)
    )
    result = await session.execute(stmt)
    existing = result.scalars().first()

    if existing:
        warn_msg = []
        if existing.phone == phone:
            warn_msg.append("❌ Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.")
        if existing.car_number == car_number:
            warn_msg.append("❌ Bu mashina raqami allaqachon ro‘yxatdan o‘tgan.") 
        return False, "❌ Bu haydovchi allaqachon ro‘yxatdan o‘tgan.", None

    # choose subclass by category
    category = category.lower()
    if category == 'comfort':
        driver = ComfortDriver(
            account_id=account_id,
            name=name, 
            phone=phone, 
            car_number=car_number,
            active_until=active_until,
            is_active=True
        )
    elif category == 'oddiy':
        driver = OddiyDriver(
            account_id=account_id, 
            name=name, 
            phone=phone, 
            car_number=car_number,
            active_until=active_until,
            is_active=True,
        )
    else:
        return False, "❌ Toifa noto‘g‘ri.", None

    try:
        session.add(driver)
        await session.commit()
        await session.refresh(driver)
        return True, f"✅ {driver.name} uchun so‘rov muvaffaqiyatli yuborildi!", driver.id
    except IntegrityError:
        await session.rollback()
        return False, "❌ Xatolik: ma’lumotlarni tekshirib qayta urinib ko‘ring.", None


async def get_driver_by_id(session: AsyncSession, driver_id: int) -> Driver | None:
    """Fetch driver by ID. Returns Driver object or None."""
    stmt = select(Driver).where(Driver.id == driver_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()




async def get_driver_by_account_id(session: AsyncSession, account_id: int) -> Driver | None:
    """Fetch a driver by account_id. Returns Driver object or None"""
    stmt = select(Driver).where(Driver.account_id == account_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()




async def update_driver_by_phone_number(session: AsyncSession, phone: str, new_values: dict) -> Optional[Driver]:
    try:
        stmt = (
            update(Driver)
            .where(Driver.phone == phone)
            .values(**new_values)
            .returning(Driver)  # <-- better: return updated row
        )
        result = await session.execute(stmt)
        updated_driver = result.scalar_one_or_none()

        await session.commit()
        return updated_driver

    except Exception as e:
        await session.rollback()
        print(f"Error updating driver: {e}")
        return None


async def delete_driver_by_car_number(session: AsyncSession, car_number: str) -> bool:
    """Delete a driver by car number. Returns True if deleted, False if not found."""
    try:
        stmt = delete(Driver).where(Driver.car_number == car_number)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
    except Exception as e:
        await session.rollback()
        print(f"Delete error: {e}")
        return False


async def set_active_until(session: AsyncSession, driver_id: int, days: int) -> bool:
    """Set active until to now + days for a driver. Returns True if updated, False if not Foun."""    
    driver = await get_driver_by_id(session, driver_id)
    if not driver:
        return False
    driver.active_until = datetime.now(timezone.utc) + timedelta(days=days)
    await session.commit()
    return True


async def extend_active_until(session: AsyncSession, driver_id: int, additional_days: int) -> bool:
    """Extend active_until: If expired or None, set from now + days; else add to existing. Returns True if updated"""
    driver = await get_driver_by_id(session, driver_id)
    if not driver:
        return False
    now = datetime.now(timezone.utc)
    if driver.active_until is None or driver.active_until < now:
        driver.active_until = now + timedelta(days=additional_days)
    else:
        driver.active_until += timedelta(days=additional_days)
    await session.commit()
    return True


async def is_driver_active(session: AsyncSession, driver_id: int) -> bool:
    """Cehck if a driver's acitve_until > now. Returns False if not Found or inactive/pending"""
    driver = await get_driver_by_id(session, driver_id)
    if not driver or driver.active_until is None:
        return False
    return driver.active_until > datetime.now(timezone.utc)


