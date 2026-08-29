from clients.supabase_storage_client import SupabaseStorageClient

class StorageService:
    def __init__(self, supabase_client: SupabaseStorageClient):
        self.__supabaseClient = supabase_client
        
    def save_image(self, file: bytes, content_type: str, filename: str, bucket: str):
        return self.__supabaseClient.save_image(file, content_type, filename, bucket)