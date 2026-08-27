from exceptions.access_denied_exception import AccessDeniedException
from exceptions.resource_not_found_exception import OrderNotFoundException, RouteNotFoundException
from repositories.order_repository import OrderRepository
from repositories.route_repository import RouteRepository
from schemas.order import OrderSaveSchema, OrderInfoSchema, OrderDeliveryProofSchema

class OrderService:
    def __init__(self, routeRepository: RouteRepository, orderRepository: OrderRepository):
        self.__route_repository = routeRepository
        self.__order_repository = orderRepository
        
    async def add_order(self, user_id: int, order_save: OrderSaveSchema):
        db_route = await self.__route_repository.find_today_by_courier_id(user_id)
        if db_route is None:
            db_route = await self.__route_repository.create_route(user_id)
        await self.__order_repository.create_order(db_route.id, order_save)
        
    async def update_order(self, user_id: int, order_id: int, order_save: OrderSaveSchema):
        db_order = await self.__order_repository.find_by_id(order_id)
        if db_order is None:
            raise OrderNotFoundException()
        db_route = await self.__route_repository.find_by_id(db_order.route_id)
        if db_route is None:
            raise RouteNotFoundException()
        if db_route.courier_id != user_id:
            raise AccessDeniedException()
        
        for key, value in order_save.model_dump().items():
            setattr(db_order, key, value)
            
        await self.__order_repository.update_order(db_order)
        
    async def delete_order(self, user_id: int, order_id: int):
        db_order = await self.__order_repository.find_by_id(order_id)
        if db_order is None:
            raise OrderNotFoundException()
        db_route = await self.__route_repository.find_by_id(db_order.route_id)
        if db_route is None:
            raise RouteNotFoundException()
        if db_route.courier_id != user_id:
            raise AccessDeniedException()
        await self.__order_repository.delete_order(db_order)
        
    async def get_today_orders(self, user_id: int):
        db_route = await self.__route_repository.find_today_by_courier_id(user_id)
        if db_route is None:
            raise RouteNotFoundException()
        db_orders = await self.__order_repository.find_active_by_route_id(db_route.id)
        if not db_orders:
            raise OrderNotFoundException()
        return [OrderInfoSchema.model_validate(db_order) for db_order in db_orders]
    
    async def get_orders_by_route_id(self, route_id: int):
        db_orders = await self.__order_repository.find_by_route_id(route_id)
        if not db_orders:
            raise OrderNotFoundException()
        return [OrderInfoSchema.model_validate(db_order) for db_order in db_orders]
    
    async def proof_delivery_order(self, user_id: int, order_id: int, order_delivery_proof: OrderDeliveryProofSchema):
        db_order = await self.__order_repository.find_by_id(order_id)
        if db_order is None:
            raise OrderNotFoundException()
        db_route = await self.__route_repository.find_by_id(db_order.route_id)
        if db_route is None:
            raise RouteNotFoundException()
        if db_route.courier_id != user_id:
            raise AccessDeniedException()
        for key, value in order_delivery_proof.model_dump().items():
            setattr(db_order, key, value)    
        db_order.status = 'Delivered'
        await self.__order_repository.update_order(db_order)
        
        
        
        