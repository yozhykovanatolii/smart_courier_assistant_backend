from typing import Annotated
from fastapi import APIRouter, Depends
from api.dependencies import get_current_user, get_route_service
from schemas.route import RouteAnalysisSchema, RouteOptimizationSchema, RoutePolylineSchema
from schemas.user import UserInfoSchema
from services.route_service import RouteService

route_router = APIRouter(prefix='/routes')
RouteServiceDependency = Annotated[RouteService, Depends(get_route_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@route_router.get('')
async def get_courier_routes(routeService: RouteServiceDependency, currentUser: CurrentUser):
    routes = await routeService.get_courier_routes(currentUser.id)
    return routes

@route_router.post('/optimize')
async def optimize_route(route_optimization: RouteOptimizationSchema, routeService: RouteServiceDependency, currentUser: CurrentUser):
    orders = await routeService.optimize_route(currentUser.id, route_optimization)
    return orders
    
@route_router.post('/analysis')    
async def analyze_route(route_analysis: RouteAnalysisSchema, routeService: RouteServiceDependency, currentUser: CurrentUser):
    route_recommendations = await routeService.analyze_route(currentUser.id, route_analysis)
    return {'recommendation': route_recommendations}
    
@route_router.get('/today/recommendation')
async def get_route_today_recommendation(routeService: RouteServiceDependency, currentUser: CurrentUser):
    route_recommendation = await routeService.get_route_today_recommendation(currentUser.id)
    return {'recommendation': route_recommendation}    
    
    
@route_router.post('/today/polyline')
async def get_route_polyline(route_polyline_request: RoutePolylineSchema, routeService: RouteServiceDependency):
    route_polyline = await routeService.get_route_polyline(route_polyline_request)
    return route_polyline
