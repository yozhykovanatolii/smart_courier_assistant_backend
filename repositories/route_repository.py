from sqlalchemy.ext.asyncio import AsyncSession
from models import Routes
from sqlalchemy import select
from datetime import datetime, timedelta

class RouteRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
    
    async def create_route(self, courier_id: int):
        db_route = Routes(courier_id = courier_id)
        self.__db.add(db_route)
        await self.__db.commit()
        await self.__db.refresh(db_route)
        return db_route
    
    async def find_today_by_courier_id(self, courier_id: int):
        today = datetime.now()
        start_of_day = datetime(today.year, today.month, today.day)
        end_of_day = start_of_day + timedelta(days = 1)
        query = select(Routes).where(Routes.courier_id == courier_id, Routes.created_at >= start_of_day, Routes.created_at < end_of_day)
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()
    
    async def find_by_id(self, route_id: int):
        return await self.__db.get(Routes, route_id)
    
    async def find_by_courier_id(self, courier_id: int):
        query = select(Routes).where(Routes.courier_id == courier_id)
        result = await self.__db.execute(query)
        return result.scalars().all()
    
    async def update_route(self, db_route: Routes):
        await self.__db.commit()
        await self.__db.refresh(db_route)
