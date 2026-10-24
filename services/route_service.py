from clients.chat_gpt_client import ChatGptClient
from exceptions.access_denied_exception import AccessDeniedException
from exceptions.resource_not_found_exception import OrderNotFoundException, RouteNotFoundException
from clients.open_route_client import OpenRouteClient
from repositories.order_repository import OrderRepository
from repositories.route_repository import RouteRepository
from schemas.order import OrderInfoSchema, OrderOptimizationSchema
from schemas.route import RouteAnalysisSchema, RouteInfoSchema, RouteOptimizationSchema, RoutePointSchema, RoutePolylineSchema
from utils import calculate_eta_by_arrival, calculate_eta_by_duration, calculate_service

class RouteService:
    def __init__(self, route_repository: RouteRepository, order_repository: OrderRepository, open_route_client: OpenRouteClient, chat_gpt_client: ChatGptClient):
        self.__route_repository = route_repository
        self.__order_repository = order_repository
        self.__open_route_client = open_route_client
        self.__chat_gpt_client = chat_gpt_client
        
    async def optimize_route(self, courier_id: int, route_optimization: RouteOptimizationSchema):
        db_route = await self.__route_repository.get_today_route_by_courier_id(courier_id)
        if db_route is None:
            raise AccessDeniedException()
        route_orders = route_optimization.orders
        has_undefined_risk = any(order.delivery_risk == 'Uknown' for order in route_orders)
        courier_coordinates = [route_optimization.courier_longitude, route_optimization.courier_latitude]
        updated_orders = []
        if has_undefined_risk:
            updated_orders = await self.__optimize_orders_processing(route_orders, courier_coordinates)
        else:
            updated_orders = await self.__update_orders_eta(route_orders, courier_coordinates)
        await self.__order_repository.update_orders(updated_orders)
        db_orders = await self.__order_repository.get_active_orders_by_route_id(db_route.id)
        if not db_orders:
            raise OrderNotFoundException()
        return [OrderInfoSchema.model_validate(db_order) for db_order in db_orders]
    
    async def __optimize_orders_processing(self, route_orders, courier_coordinates: list[float]):
        jobs = self.__convert_orders_to_job(route_orders)
        steps = await self.__open_route_client.optimize_route(jobs, courier_coordinates)
        jobs_only = [item for item in steps if item.get("type") == "job"]
        updated_orders = calculate_eta_by_arrival(jobs_only, route_orders)
        return updated_orders
    
    async def __update_orders_eta(self, route_orders, courier_coordinates: list[float]):
        locations = self.__convert_orders_coordinates_to_locations(route_orders, courier_coordinates)
        locations_duration = await self.__open_route_client.get_locations_duration(locations)
        updated_orders = calculate_eta_by_duration(locations_duration, route_orders)
        old_count_delayed_orders = sum(1 for route_order in route_orders if route_order.delivery_risk == 'Delayed')
        new_count_delayed_orders = sum(1 for order in updated_orders if order.get('delivery_risk') == 'Delayed')
        if new_count_delayed_orders - old_count_delayed_orders >= 2:
            updated_orders = await self.__optimize_orders_processing(route_orders, courier_coordinates)
        return updated_orders
    
    async def get_courier_routes(self, courier_id: int):
        db_routes = await self.__route_repository.get_route_by_courier_id(courier_id)
        if not db_routes:
            raise RouteNotFoundException()
        return [RouteInfoSchema.model_validate(db_route) for db_route in db_routes]
    
    async def analyze_route(self, courier_id: int, route_analysis: RouteAnalysisSchema):
        db_route = self.__route_repository.get_today_route_by_courier_id(courier_id)
        if db_route is None:
            raise AccessDeniedException()
        prompt = self.__generate_prompt(route_analysis)
        route_recommendation = await self.__chat_gpt_client.generate_recommendations(prompt, route_analysis.language_code)
        db_route.recommendation = route_recommendation
        self.__route_repository.update_route(db_route)
        return route_recommendation
    
    async def get_route_today_recommendation(self, courier_id: int):
        db_route = await self.__route_repository.get_today_route_by_courier_id(courier_id)
        if db_route is None:
            raise RouteNotFoundException()
        return db_route.recommendation
    
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
            'service': calculate_service(order.bottle_quantity, order.floor),
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
    
    def __generate_prompt(self, analysis: RouteAnalysisSchema) -> str:
        lines = [
            "Route analysis:",
            f"Total orders: {analysis.total_orders}",
            f"Orders at risk or delayed: {len(analysis.risky_orders)}",
            "",
        ]
        for order in analysis.risky_orders:
            lines.append(
                f'Order #{order.id} at "{order.address}" '
                f'is {order.delivery_risk}, '
                f'delay about {order.delay_minutes} min, '
                f'position {order.position_in_route + 1} in route'
            )
        return "\n".join(lines)
        
        