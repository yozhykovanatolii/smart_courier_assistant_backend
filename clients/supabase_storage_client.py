from datetime import datetime
from supabase import create_client
from config import settings

class SupabaseStorageClient:
    def __init__(self):
        self.__client = create_client(settings.supabase_project_url, settings.supabase_anon_key)
        
    def save_image(self, file: bytes, content_type: str, filename: str, bucket: str):
        extension = filename.split(".")[-1]
        file_name = f"{int(datetime.now().timestamp() * 1000)}.{extension}"
        self.__client.storage.from_(bucket).upload(file = file, path = file_name, file_options = {"content-type": content_type})
        return self.__client.storage.from_(bucket).get_public_url(file_name)