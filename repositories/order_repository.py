from sqlalchemy.ext.asyncio import AsyncSession
from models import Orders
from schemas.order import OrderSaveSchema, OrderOptimizationSchema
from sqlalchemy import Update, select

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def create_order(self, route_id: int, order_create: OrderSaveSchema):
        db_order = Orders(route_id = route_id, client_full_name = order_create.client_full_name, client_phone_number = order_create.client_phone_number, delivery_by = order_create.delivery_by, address = order_create.address, latitude = order_create.latitude, longitude = order_create.longitude)
        self.__db.add(db_order)
        await self.__db.commit()
        await self.__db.refresh(db_order)
        return db_order
    
    async def get_order_by_id(self, order_id: int):
        return await self.__db.get(Orders, order_id)
    
    async def update_order(self, db_order_new: Orders):
        await self.__db.commit()
        await self.__db.refresh(db_order_new)
    
    async def delete_order(self, db_order: Orders):
        await self.__db.delete(db_order)
        await self.__db.commit()
        
    async def update_orders(self, orders: list[OrderOptimizationSchema]):
        await self.__db.execute(Update(Orders), [order.model_dump() for order in orders])
        await self.__db.commit()
        
    async def get_active_orders_by_route_id(self, route_id: int):
        query = select(Orders).where(Orders.route_id == route_id, Orders.status == 'Active')
        result = await self.__db.execute(query)
        return result.scalars().all()
    
    async def get_orders_by_route_id(self, route_id: int):
        query = select(Orders).where(Orders.route_id == route_id)
        result = await self.__db.execute(query)
        return result.scalars().all()