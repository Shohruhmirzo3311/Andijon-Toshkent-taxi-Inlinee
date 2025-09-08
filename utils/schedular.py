import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.sql import select

from data.driverDb import Driver
from data.init_tables import AsyncSessionLocal

schedular = AsyncIOScheduler()




async def check_expired_drivers():
    """Check for eexpired drivers and deactivate them"""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Driver).where(Driver.is_active == True)
            )
            drivers = result.scalars().all()
            
            now = datetime.now()
            deactivated_count = 0
            
            for driver in drivers:
                if driver.active_until and now > driver.active_until:
                    driver.is_active = False
                    deactivated_count += 1
            
            if deactivated_count > 0:
                await session.commit()
                print(f"Deactivated {deactivated_count} expired drivers")
        
        except Exception as e:
            print(f"Error checking expired drivers: {e}")
            


async def init_schedular():
    schedular.add_job(check_expired_drivers, 'interval', hours=24)
    schedular.start()

