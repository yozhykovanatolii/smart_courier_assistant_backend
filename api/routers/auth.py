from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import get_auth_service
from schemas.token import TokenSchema
from schemas.user import UserRegisterSchema, UserLoginSchema
from services.auth_service import AuthService

auth_router = APIRouter(prefix='/auth')
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]

@auth_router.post('/register', status_code = status.HTTP_201_CREATED)
async def register_user(userRegister: UserRegisterSchema, authService: AuthServiceDependency):
    await authService.register_user(userRegister)
    return {'message': 'Success registration'}
    
@auth_router.post('/login', status_code = status.HTTP_200_OK)
async def login_user(userLogin: UserLoginSchema, authService: AuthServiceDependency):
    return await authService.login_user(userLogin)
    
@auth_router.post('/refresh', status_code = status.HTTP_200_OK, response_model = TokenSchema, response_model_exclude_none = True)
async def refresh_token(token: str | None, authService: AuthServiceDependency):
    return await authService.refresh_token(token)