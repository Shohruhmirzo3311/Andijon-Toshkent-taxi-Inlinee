from typing import List, Optional

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, UniqueConstraint, delete, update)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from utils.db_api.init_tables import Base


class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, unique=True)
    
    drivers = relationship("Driver", back_populates="city", cascade="all, delete")
    routes = relationship("Route", back_populates="route", cascade="all, delete")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    from_city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    to_city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))

    from_city = relationship("City", foreign_keys=[from_city_id])
    to_city = relationship("City", foreign_keys=[to_city_id])

    # Prevent duplicate routes (e.g. Andijon→Toshkent twice)
    __table_args__ = (
        UniqueConstraint("from_city_id", "to_city_id", name="uq_route_from_to"),
    )

# ✅ Create
async def create_city(db: AsyncSession, name: str) -> City:
    new_city = City(name=name)
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city




# ✅ Read all
async def get_all_cities(db: AsyncSession) -> List[City]:
    result = await db.execute(select(City.name))
    return result.scalars().all()


# ✅ Read one
async def get_city_by_id(db: AsyncSession, city_id: int) -> Optional[City]:
    result = await db.execute(select(City).where(City.id == city_id))
    return result.scalar_one_or_none()




# Get by name
async def get_city_by_name(db: AsyncSession, name: str) -> Optional[City]:
    result = await db.execute(select(City).where(City.name.ilike(name)))
    return result.scalar_one_or_none()

# Update
async def update_city(db: AsyncSession, city_id: int, name: str) -> Optional[City]:
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        return None

    city.name = name
    await db.commit()
    await db.refresh(city)
    return city



# ✅ Delete
async def delete_city(db: AsyncSession, name: str) -> City | None:
    result = await db.execute(
        select(City).where(City.name.ilike(name))
    )
    city = result.scalar_one_or_none()
    if not city:
        return None

    await db.delete(city)
    await db.commit()
    return city





async def create_route(session: AsyncSession, from_city: str, to_city: str) -> Route:
    result = await session.execute(select(City).where(City.name == from_city))
    from_obj = result.scalar_one_or_none()
    if not from_obj:
        from_obj = City(name=from_city)
        session.add(from_city)
        await session.flush()
        
    result2 = await session.execute(select(City).where(City.name == to_city))
    to_obj = result2.scalar_one_or_none()
    if not to_obj:
        to_obj = City(name=to_city)
        session.add(to_obj)
        await session.flush()
        
    
    route = Route(from_city_id=from_obj.id, to_city_id=to_obj.id)
    session.add(route)
    await session.commit()
    await session.refresh(route)
    return route


async def get_all_routes(session: AsyncSession) -> list[Route]:
    result = await session.execute(select(Route))
    return result.scalar().all()


