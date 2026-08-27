from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from schemas.validators import AddressStr, FullNameStr

class OrderSaveSchema(BaseModel):
    client_full_name: FullNameStr
    client_phone_number: str = Field(pattern=r'^\+380\d{9}$')
    delivery_by: datetime
    address: AddressStr
    latitude: float
    longitude: float
    
class OrderInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    route_id: int
    client_full_name: FullNameStr
    client_phone_number: str = Field(pattern=r'^\+380\d{9}$')
    delivery_by: datetime
    delivery_risk: str
    status: str
    planned_eta: datetime
    address: AddressStr
    latitude: float
    longitude: float
    courier_comment: str | None
    confirmed_at: datetime | None
    order_photos_url: list[str] | None
    order_index: int
    
class OrderDeliveryProofSchema(BaseModel):
    courier_comment: str = Field(min_length=1, max_length=200)
    confirmed_at: datetime
    order_photos_url: list[str] = Field(min_length=1)
    
class OrderOptimizationSchema(BaseModel):
    id: int
    latitude: float
    longitude: float
    delivery_by: datetime
    delivery_risk: str
    planned_eta: datetime
    order_index: int
    
class RiskyOrderSchema(BaseModel):
    id: int
    address: AddressStr
    delivery_risk: str
    delay_minutes: int
    position_in_route: int