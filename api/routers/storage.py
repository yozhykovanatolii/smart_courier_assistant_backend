from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from api.dependencies import get_storage_service
from services.storage_service import StorageService

storage_router = APIRouter(prefix='/storage')
StorageServiceDependency = Annotated[StorageService, Depends(get_storage_service)]

@storage_router.post('/upload', status_code = status.HTTP_200_OK)
async def upload_image(storageService: StorageServiceDependency, file: UploadFile = File(...), bucket: str = Form(...)):
    file_bytes = await file.read()
    image_url = storageService.save_image(file_bytes, file.content_type, file.filename, bucket)
    return {'url': image_url}