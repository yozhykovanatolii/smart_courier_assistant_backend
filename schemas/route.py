from pydantic import BaseModel, ConfigDict
from schemas.order import OrderOptimizationSchema, RiskyOrderSchema
from datetime import datetime

class RouteOptimizationSchema(BaseModel):
    courier_latitude: float
    courier_longitude: float
    orders: list[OrderOptimizationSchema]
    
class RoutePointSchema(BaseModel):
    latitude: float
    longitude: float
    
class RoutePolylineSchema(BaseModel):
    route_points: list[RoutePointSchema]

class RouteInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    courier_id: int
    created_at: datetime
    recommendation: str
    
class RouteAnalysisSchema(BaseModel):
    language_code: str
    total_orders: int
    risky_orders: list[RiskyOrderSchema]
    