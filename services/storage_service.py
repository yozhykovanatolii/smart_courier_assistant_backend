from clients.supabase_storage_client import SupabaseStorageClient
from exceptions.media_type_exception import MediaTypeException

class StorageService:
    def __init__(self, supabase_client: SupabaseStorageClient):
        self.__supabaseClient = supabase_client
        
    def save_image(self, user_id: int, file: bytes, content_type: str, filename: str, bucket: str):
        ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
        if content_type not in ALLOWED_TYPES:
            raise MediaTypeException()
        return self.__supabaseClient.save_image(user_id, file, content_type, filename, bucket)