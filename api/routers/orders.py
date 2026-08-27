from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import get_current_user, get_order_service
from schemas.order import OrderSaveSchema, OrderDeliveryProofSchema
from schemas.user import UserInfoSchema
from services.order_service import OrderService

order_router = APIRouter(prefix='/orders')
OrderServiceDependency = Annotated[OrderService, Depends(get_order_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@order_router.post('', status_code = status.HTTP_200_OK)
async def create_order(order_save: OrderSaveSchema, orderService: OrderServiceDependency, currentUser: CurrentUser):
    await orderService.add_order(currentUser.id, order_save)
    return {'message': 'Success creating of the order'}
    
@order_router.get('', status_code = status.HTTP_200_OK)
async def get_orders_by_route_id(route_id: int, orderService: OrderServiceDependency):
    orders = await orderService.get_orders_by_route_id(route_id)
    return orders
        
@order_router.delete('/{order_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, orderService: OrderServiceDependency, currentUser: CurrentUser):
    await orderService.delete_order(currentUser.id, order_id) 
    
@order_router.patch('/{order_id}', status_code = status.HTTP_200_OK)
async def update_order(order_id: int, order_save: OrderSaveSchema, orderService: OrderServiceDependency, currentUser: CurrentUser):
    await orderService.update_order(currentUser.id, order_id, order_save) 
    return {'message': 'Success updating of the order'}
    
@order_router.get('/today', status_code = status.HTTP_200_OK)
async def get_today_orders(orderService: OrderServiceDependency, currentUser: CurrentUser):
    orders = await orderService.get_today_orders(currentUser.id)
    return orders
    
@order_router.patch('/{order_id}/proof-delivery', status_code = status.HTTP_200_OK)
async def proof_delivery_order(order_id: int, order_delivery_proof: OrderDeliveryProofSchema, orderService: OrderServiceDependency, currentUser: CurrentUser):
    await orderService.proof_delivery_order(currentUser.id, order_id, order_delivery_proof) 
    return {'message': 'Success proving delivery of the order'}   
