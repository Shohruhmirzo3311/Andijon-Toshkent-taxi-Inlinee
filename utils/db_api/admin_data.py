import asyncio
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

# Your code
from utils.db_api.init_tables import AsyncSessionLocal
from utils.db_api.administrationDb import Bot_Admin
from sqlalchemy import select

ADMINS: list[int] = []

async def laod_admins():
    global ADMINS
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Bot_Admin.account_id))
        ADMINS = [row[0] for row in result.all()]
    return ADMINS

# The test function
async def test_laod_admins():
    admins_list = await laod_admins()
    print("Admin accounts found:", admins_list)
    print("Global ADMINS list:", ADMINS)

# Run the test function
if __name__ == "__main__":
    asyncio.run(test_laod_admins())