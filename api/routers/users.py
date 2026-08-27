from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import get_current_user, get_user_service
from services.user_service import UserService
from schemas.user import UserInfoSchema, UserUpdateSchema

user_router = APIRouter(prefix='/users')
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@user_router.get('/me', status_code = status.HTTP_200_OK)
async def get_user(currentUser: CurrentUser):
    return currentUser
    
@user_router.patch('/me', status_code = status.HTTP_204_NO_CONTENT)
async def update_user(user_data: UserUpdateSchema, userService: UserServiceDependency, currentUser: CurrentUser):
    await userService.update_user(currentUser.id, user_data)