from math import ceil
from exceptions.access_denied_exception import AccessDeniedException
from exceptions.resource_not_found_exception import OrderNotFoundException, RouteNotFoundException
from clients.open_route_client import OpenRouteClient
from repositories.order_repository import OrderRepository
from repositories.route_repository import RouteRepository
from schemas.order import OrderInfoSchema, OrderOptimizationSchema
from schemas.route import RouteAnalysisSchema, RouteInfoSchema, RouteOptimizationSchema, RoutePointSchema, RoutePolylineSchema
from datetime import datetime, timedelta, timezone
import time

class RouteService:
    def __init__(self, route_repository: RouteRepository, order_repository: OrderRepository, open_route_client: OpenRouteClient):
        self.__route_repository = route_repository
        self.__order_repository = order_repository
        self.__open_route_client = open_route_client
        
    async def optimize_route(self, courier_id: int, route_optimization: RouteOptimizationSchema):
        db_route = await self.__route_repository.get_today_route_by_courier_id(courier_id)
        if db_route is None:
            raise AccessDeniedException()
        
        route_orders = route_optimization.orders
        has_undefined_risk = any(order.delivery_risk == 'Uknown' for order in route_orders)
        courier_coordinates = [route_optimization.courier_longitude, route_optimization.courier_latitude]
        updated_orders = []
        
        if has_undefined_risk:
            updated_orders = await self.__optimize_routes(route_orders, courier_coordinates)
        else:
            updated_orders = await self.__update_orders_eta(route_orders, courier_coordinates)
        await self.__order_repository.update_orders(updated_orders)
    
    async def __optimize_routes(self, route_orders, courier_coordinates: list[float]):
        jobs = self.__convert_orders_to_job(route_orders)
        steps = await self.__open_route_client.optimize_route(jobs, courier_coordinates)
        jobs_only = [item for item in steps if item.get("type") == "job"]
        updated_orders = self.__calculate_eta_by_arrival(jobs_only, route_orders)
        return updated_orders
    
    async def __update_orders_eta(self, route_orders, courier_coordinates: list[float]):
        locations = self.__convert_orders_coordinates_to_locations(route_orders, courier_coordinates)
        locations_duration = await self.__open_route_client.get_locations_duration(locations)
        updated_orders = self.__calculate_eta_by_duration(locations_duration, route_orders)
        old_count_delayed_orders = sum(1 for route_order in route_orders if route_order.delivery_risk == 'Delayed')
        new_count_delayed_orders = sum(1 for order in updated_orders if order.get('delivery_risk') == 'Delayed')
        if new_count_delayed_orders - old_count_delayed_orders >= 2:
            updated_orders = await self.__optimize_routes(route_orders, courier_coordinates)
        return updated_orders
    
    async def get_courier_routes(self, courier_id: int):
        db_routes = await self.__route_repository.get_route_by_courier_id(courier_id)
        if not db_routes:
            raise RouteNotFoundException()
        return [RouteInfoSchema.model_validate(db_route) for db_route in db_routes]
    
    async def get_route_polyline(self, route_polyline: RoutePolylineSchema):
        coordinates = [
            [point.longitude, point.latitude]
            for point in route_polyline.route_points
        ]
        polyline = await self.__open_route_client.get_route_polyne(coordinates)
        route_points = [
            RoutePointSchema(latitude = point[1], longitude = point[0])
            for point in polyline
        ]
        return RoutePolylineSchema(route_points = route_points)
        
        
    def __convert_orders_to_job(self, orders: list[OrderOptimizationSchema]) -> list[dict]:
        return [
        {
            'id': order.id,
            'location': [order.longitude, order.latitude],
            'service': self.__calculate_service(order.bottle_quantity, order.floor),
        }
        for order in orders
    ]
        
    def __convert_orders_coordinates_to_locations(self, orders: list[OrderOptimizationSchema], courier_coordinates: list[float]):
        locations = [
           [order.longitude, order.latitude]
           for order in orders 
        ]
        locations.insert(0, courier_coordinates)
        return locations
        
    def __calculate_service(self, bottle_quantity: int, floor: int | None):
        trips = ceil(bottle_quantity / 2)
        if floor is None:
            return trips * 30 + (trips - 1) * 20 + 90
        floors_up = floor - 1
        loading_time = trips * (30 + floors_up * 23)
        return_time = (trips - 1) * (20 + floors_up * 12)
        return loading_time + return_time + 90     
    
    def __calculate_eta_by_duration(self, duration: list[float], orders: list[OrderOptimizationSchema]):
        start_time = datetime.now(timezone.utc)
        updated_orders = []
        for order, route_duration in zip(orders, duration):
            service_seconds = self.__calculate_service(order.bottle_quantity, order.floor)
            eta = start_time + timedelta(seconds=route_duration) + timedelta(seconds=service_seconds)
            delivery_risk = self.__get_delivery_risk_by_eta(eta, order.delivery_by)
            updated_orders.append(
            {
                'id': order.id,
                'latitude': order.latitude,
                'longitude': order.longitude,
                'planned_eta': eta.replace(tzinfo=None),
                'delivery_risk': delivery_risk,
                'order_index': order.order_index,
            })
        return updated_orders
        
        
    def __calculate_eta_by_arrival(self, steps: list[dict], orders: list[OrderOptimizationSchema]):
        start_time = datetime.now(timezone.utc)
        order_by_id = {order.id: order for order in orders}
        updates = []
        for step in steps:
            order = order_by_id[step["id"]]
            arrival_seconds = step.get("arrival", 0)
            eta = start_time + timedelta(seconds=arrival_seconds)
            delivery_risk = self.__get_delivery_risk_by_eta(eta, order.delivery_by)
            updates.append(
            {
                'id': order.id,
                'latitude': step["location"][1],
                'longitude': step["location"][0],
                'planned_eta': eta.replace(tzinfo=None),
                'delivery_risk': delivery_risk,
                'order_index': len(updates),
            })
        return updates
            
            
    def __get_delivery_risk_by_eta(self, eta: datetime, delivery_by: time):
        delivery_datetime = datetime.combine(eta.date(), delivery_by)
        difference = delivery_datetime - eta
        difference_minutes = difference.total_seconds() / 60
        if difference_minutes >= 5:
            return 'On time'
        if difference_minutes >= 0:
            return 'At risk'
        return 'Delayed'
        
        