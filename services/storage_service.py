from clients.supabase_storage_client import SupabaseStorageClient

class StorageService:
    def __init__(self, supabaseClient: SupabaseStorageClient):
        self.__supabaseClient = supabaseClient
        
    def save_image(self, file: bytes, content_type: str, filename: str, bucket: str):
        return self.__supabaseClient.save_image(file, content_type, filename, bucket)