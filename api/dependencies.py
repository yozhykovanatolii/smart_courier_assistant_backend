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

def get_user_service(user_Repository: UserRepositoryDependency):
    return UserService(user_Repository)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_Service: Annotated[UserService, Depends(get_user_service)]):
    return await user_Service.get_user(token)

def get_auth_service(user_repository: UserRepositoryDependency):
    return AuthService(user_repository)

def get_order_service(order_repository: OrderRepositoryDependency, route_repository: RouteRepositoryDependency):
    return OrderService(route_repository, order_repository)

def get_route_service(order_repository: OrderRepositoryDependency, route_repository: RouteRepositoryDependency, open_route_client: OpenRouteClientDependency, chat_gpt_client: ChatGptClientDependency):
    return RouteService(route_repository, order_repository, open_route_client, chat_gpt_client)

def get_storage_service(supabase_storage_client: SupabaseStorageClientDependency):
    return StorageService(supabase_storage_client)

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]
OrderRepositoryDependency = Annotated[OrderRepository, Depends(get_order_repository)]
RouteRepositoryDependency = Annotated[RouteRepository, Depends(get_route_repository)]
OpenRouteClientDependency = Annotated[OpenRouteClient, Depends(get_open_route_client)]
ChatGptClientDependency = Annotated[ChatGptClient, Depends(get_chat_gpt_client)]
SupabaseStorageClientDependency = Annotated[SupabaseStorageClient, Depends(get_supabase_storage_client)]
