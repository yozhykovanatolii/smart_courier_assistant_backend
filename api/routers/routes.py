from typing import Annotated
from fastapi import APIRouter, Depends
from api.dependencies import get_current_user, get_route_service
from schemas.route import RouteOptimizationSchema, RoutePolylineSchema
from schemas.user import UserInfoSchema
from services.route_service import RouteService

route_router = APIRouter(prefix='/routes')
RouteServiceDependency = Annotated[RouteService, Depends(get_route_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@route_router.get('')
async def get_courier_routes(route_service: RouteServiceDependency, current_user: CurrentUser):
    routes = await route_service.get_courier_routes(current_user.id)
    return routes

@route_router.post('/today/optimize')
async def optimize_today_route(route_optimization: RouteOptimizationSchema, route_service: RouteServiceDependency, current_user: CurrentUser):
    return await route_service.optimize_route(current_user.id, route_optimization)
    
@route_router.post('/today/polyline')
async def get_route_polyline(route_polyline_request: RoutePolylineSchema, route_service: RouteServiceDependency):
    route_polyline = await route_service.get_route_polyline(route_polyline_request)
    return route_polyline
