from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)

class User(Base):
    __tablename__ = 'users'
    
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    avatar_url = Column(String, nullable=False)
    
    
class Route(Base):
    __tablename__ = 'routes'
    
    courier_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recommendation = Column(String, default = '', nullable=False)
    created_at = Column(DateTime, default = datetime.now)
    
    
class Order(Base):
    __tablename__ = 'orders'
    
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)
    client_full_name = Column(String, nullable=False)
    client_phone_number = Column(String, nullable=False)
    delivery_by = Column(DateTime, nullable=False)
    delivery_risk = Column(String, default = 'Uknown')
    status = Column(String, default = 'Active')
    planned_eta = Column(DateTime, default = datetime.now)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    courier_comment = Column(String, default=None, nullable=True)
    confirmed_at = Column(DateTime, default=None, nullable=True)
    order_photos_url = Column(ARRAY(String), default=None, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)