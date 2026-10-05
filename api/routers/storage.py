from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from api.dependencies import get_current_user, get_storage_service
from schemas.user import UserInfoSchema
from services.storage_service import StorageService

storage_router = APIRouter(prefix='/storage')
StorageServiceDependency = Annotated[StorageService, Depends(get_storage_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@storage_router.post('/upload', status_code = status.HTTP_200_OK)
async def upload_image(storage_service: StorageServiceDependency, current_user: CurrentUser, file: UploadFile = File(...), bucket: str = Form(...)):
    file_bytes = await file.read()
    image_url = storage_service.save_image(current_user.id, file_bytes, file.content_type, file.filename, bucket)
    return {'image_url': image_url}