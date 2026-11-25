from datetime import datetime, timedelta, timezone
from math import ceil
from schemas.order import OrderOptimizationSchema
import time


def calculate_service(bottle_quantity: int):
    trips = ceil(bottle_quantity / 2)
    return trips * 30 + (trips - 1) * 20 + 90    
    
def calculate_eta_by_duration(duration: list[float], orders: list[OrderOptimizationSchema]):
    start_time = datetime.now(timezone.utc)
    updated_orders = []
    for order, route_duration in zip(orders, duration):
        service_seconds = calculate_service(order.bottle_quantity)
        eta = start_time + timedelta(seconds=route_duration) + timedelta(seconds=service_seconds)
        delivery_risk = _get_delivery_risk_by_eta(eta, order.delivery_by)
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
        
        
def calculate_eta_by_arrival(steps: list[dict], orders: list[OrderOptimizationSchema]):
    start_time = datetime.now(timezone.utc)
    order_by_id = {order.id: order for order in orders}
    updates = []
    for step in steps:
        order = order_by_id[step["id"]]
        arrival_seconds = step.get("arrival", 0)
        eta = start_time + timedelta(seconds=arrival_seconds)
        delivery_risk = _get_delivery_risk_by_eta(eta, order.delivery_by)
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
            
            
def _get_delivery_risk_by_eta(eta: datetime, delivery_by: time):
    delivery_datetime = datetime.combine(eta.date(), delivery_by)
    difference = delivery_datetime - eta
    difference_minutes = difference.total_seconds() / 60
    if difference_minutes >= 5:
        return 'On time'
    if difference_minutes >= 0:
        return 'At risk'
    return 'Delayed'