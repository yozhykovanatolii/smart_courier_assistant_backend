from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import Users
from schemas.user import UserRegisterSchema


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def create_user(self, userRegister: UserRegisterSchema):
        db_user = Users(full_name = userRegister.full_name, phone_number = userRegister.phone_number, email = userRegister.email, password = userRegister.password, avatar_url = 'https://fojohxjzxvieoakjyzwz.supabase.co/storage/v1/object/public/images/users/default_avatar.jpg')
        self.__db.add(db_user)
        await self.__db.commit()
        await self.__db.refresh(db_user)
        return db_user
    
    async def find_by_id(self, user_id: int):
        return await self.__db.get(Users, user_id)
    
    async def update_user(self, update_data: dict):
        await self.__db.execute(update(Users), [update_data])
        await self.__db.commit()
    
    async def find_by_email(self, email: str):
        query = select(Users).where(Users.email == email)
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()