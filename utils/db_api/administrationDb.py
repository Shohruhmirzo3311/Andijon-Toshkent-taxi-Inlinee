from typing import List, Optional

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, UniqueConstraint, delete, update)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from utils.db_api.init_tables import Base, AsyncSessionLocal



class Bot_Admin(Base):
    __tablename__ = 'administration'
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Bot_Admin id={self.id} name={self.name} account_id={self.account_id}>"


async def create_admin(session: AsyncSession, account_id: int, name: str) -> Bot_Admin:
    new_admin = Bot_Admin(account_id=account_id, name=name)
    session.add(new_admin)
    await session.commit()
    await session.refresh(new_admin)
    return new_admin




async def get_admin(session: AsyncSession, name: str):
    result = await session.execute(
        select(Bot_Admin).where(Bot_Admin.name == name.lower())
    )
    return result.scalar_one_or_none()




async def update_admin(session: AsyncSession, admin_id: int, new_name: str):
    result = await session.execute(select(Bot_Admin).where(Bot_Admin.id == admin_id))
    admin_update = result.scalar_one_or_none()
    if not admin_update:
        return None

    admin_update.name = new_name
    await session.commit()
    await session.refresh(admin_update)
    return admin_update




async def delete_admin(session: AsyncSession, account_id: int) -> bool:
    result = await session.execute(select(Bot_Admin).where(Bot_Admin.account_id == account_id))
    d_admin = result.scalar_one_or_none()
    if not d_admin:
        return None
    
    await session.delete(d_admin)
    await session.commit()
    return d_admin