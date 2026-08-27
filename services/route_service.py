from clients.chat_gpt_client import ChatGptClient
from exceptions.access_denied_exception import AccessDeniedException
from exceptions.resource_not_found_exception import OrderNotFoundException, RouteNotFoundException
from clients.open_route_client import OpenRouteClient
from repositories.order_repository import OrderRepository
from repositories.route_repository import RouteRepository
from schemas.order import OrderInfoSchema, OrderOptimizationSchema
from schemas.route import RouteAnalysisSchema, RouteInfoSchema, RouteOptimizationSchema, RoutePointSchema, RoutePolylineSchema
from datetime import datetime, timedelta, timezone

class RouteService:
    def __init__(self, routeRepository: RouteRepository, orderRepository: OrderRepository, openRouteClient: OpenRouteClient, chatGptClient: ChatGptClient):
        self.__route_repository = routeRepository
        self.__order_repository = orderRepository
        self.__open_route_client = openRouteClient
        self.__chat_gpt_client = chatGptClient
        
    async def optimize_route(self, courier_id: int, route_optimization: RouteOptimizationSchema):
        db_route = await self.__route_repository.find_today_by_courier_id(courier_id)
        if db_route is None:
            raise AccessDeniedException()
        jobs = self.__convert_orders_to_job(route_optimization.orders)
        steps = await self.__open_route_client.optimize_route(jobs, [route_optimization.courier_longitude, route_optimization.courier_latitude])
        updated_orders = self.__calculate_eta(steps, route_optimization.orders)
        await self.__order_repository.update_orders(updated_orders)
        db_orders = await self.__order_repository.find_active_by_route_id(db_route.id)
        if not db_orders:
            raise OrderNotFoundException()
        return [OrderInfoSchema.model_validate(db_order) for db_order in db_orders]
    
    async def analyze_route(self, courier_id: int, route_analysis: RouteAnalysisSchema):
        db_route = self.__route_repository.find_today_by_courier_id(courier_id)
        if db_route is None:
            raise AccessDeniedException()
        prompt = self.__generate_prompt(route_analysis)
        route_recommendation = await self.__chat_gpt_client.generate_recommendations(prompt, route_analysis.language_code)
        db_route.recommendation = route_recommendation
        self.__route_repository.update_route(db_route)
        return route_recommendation
    
    async def get_route_today_recommendation(self, courier_id: int):
        db_route = await self.__route_repository.find_today_by_courier_id(courier_id)
        if db_route is None:
            raise RouteNotFoundException()
        return db_route.recommendation
    
    async def get_courier_routes(self, courier_id: int):
        db_routes = await self.__route_repository.find_by_courier_id(courier_id)
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
        }
        for order in orders
    ]
        
    def __calculate_eta(self, steps: list[dict], orders: list[OrderOptimizationSchema]):
        start_time = datetime.now(timezone.utc)
        cumulative_duration = timedelta()
        order_by_id = {order.id: order for order in orders}
        updates = []
        for step in steps:
            if step["type"] != "job":
                continue
            order = order_by_id[step["job"]]
            cumulative_duration += timedelta(seconds=step["duration"] + 300)
            eta = start_time + cumulative_duration
            delivery_risk = self.__get_delivery_risk_by_eta(eta, order.delivery_by)
            updates.append(
            {
                'id': order.id,
                'latitude': step["location"][1],
                'longitude': step["location"][0],
                'planned_eta': eta,
                'delivery_risk': delivery_risk,
                'order_index': len(updates),
            })
        return updates
            
            
    def __get_delivery_risk_by_eta(self, eta: datetime, delivery_by: datetime):
        difference = delivery_by - eta
        difference_minutes = difference.total_seconds() / 60
        if difference_minutes >= 5:
            return 'On time'
        if difference_minutes >= 0:
            return 'At risk'
        return 'Delayed'
    
    
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
        
        