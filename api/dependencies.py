from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from clients.chat_gpt_client import ChatGptClient
from clients.supabase_storage_client import SupabaseStorageClient
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from clients.open_route_client import OpenRouteClient
from repositories.order_repository import OrderRepository
from repositories.route_repository import RouteRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.order_service import OrderService
from services.route_service import RouteService
from services.storage_service import StorageService
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_order_repository(db: DatabaseSession):
    return OrderRepository(db)

def get_route_repository(db: DatabaseSession):
    return RouteRepository(db)

def get_user_repository(db: DatabaseSession):
    return UserRepository(db)

def get_open_route_client():
    return OpenRouteClient()

def get_chat_gpt_client():
    return ChatGptClient()

def get_supabase_storage_client():
    return SupabaseStorageClient()

def get_user_service(userRepository: UserRepositoryDependency):
    return UserService(userRepository)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], userService: Annotated[UserService, Depends(get_user_service)]):
    return await userService.get_user(token)

def get_auth_service(userRepository: UserRepositoryDependency):
    return AuthService(userRepository)

def get_order_service(orderRepository: OrderRepositoryDependency, routeRepository: RouteRepositoryDependency):
    return OrderService(routeRepository, orderRepository)

def get_route_service(orderRepository: OrderRepositoryDependency, routeRepository: RouteRepositoryDependency, openRouteClient: OpenRouteClientDependency, chatGptClient: ChatGptClientDependency):
    return RouteService(routeRepository, orderRepository, openRouteClient, chatGptClient)

def get_storage_service(supabaseStorageClient: SupabaseStorageClientDependency):
    return StorageService(supabaseStorageClient)

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]
OrderRepositoryDependency = Annotated[OrderRepository, Depends(get_order_repository)]
RouteRepositoryDependency = Annotated[RouteRepository, Depends(get_route_repository)]
OpenRouteClientDependency = Annotated[OpenRouteClient, Depends(get_open_route_client)]
ChatGptClientDependency = Annotated[ChatGptClient, Depends(get_chat_gpt_client)]
SupabaseStorageClientDependency = Annotated[SupabaseStorageClient, Depends(get_supabase_storage_client)]
