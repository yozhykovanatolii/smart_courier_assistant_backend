from fastapi import APIRouter
from api.routers import users, auth, storage, orders, routes

api_router = APIRouter()
api_router.include_router(users.user_router)
api_router.include_router(auth.auth_router)
api_router.include_router(storage.storage_router)
api_router.include_router(orders.order_router)
api_router.include_router(routes.route_router)