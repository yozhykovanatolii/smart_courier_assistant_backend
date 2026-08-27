from exceptions.authentication_exception import PasswordNotVerifiedException, TokenTypeException, UserNotFoundException
from exceptions.email_already_used_exception import EmailAlreadyUsedException
from repositories.user_repository import UserRepository
from schemas.token import TokenSchema
from schemas.user import UserRegisterSchema, UserLoginSchema
from security import get_password_hash, verify_password, create_token, decode_refresh_token

class AuthService:
    def __init__(self, userRepository: UserRepository):
        self.__user_repository = userRepository
        
    async def register_user(self, userRegister: UserRegisterSchema):
        db_user = await self.__user_repository.find_by_email(userRegister.email)
        if db_user is not None:
            raise EmailAlreadyUsedException()
        userRegister.password = get_password_hash(userRegister.password)
        await self.__user_repository.create_user(userRegister)
        
    async def login_user(self, userLogin: UserLoginSchema):
        db_user = await self.__user_repository.find_by_email(userLogin.email)
        if db_user is None:
            raise UserNotFoundException()
        isPasswordVerified = verify_password(userLogin.password, db_user.password)
        if not isPasswordVerified:
            raise PasswordNotVerifiedException()
        access_token = create_token(token_data = {'sub': str(db_user.id)}, expires_time_minutes = 30, token_type = 'access')
        refresh_token = create_token(token_data = {'sub': str(db_user.id)}, expires_time_minutes = 43200, token_type = 'refresh')
        return TokenSchema(access_token = access_token, refresh_token = refresh_token)
        
    async def refresh_token(self, token: str):
        payload = decode_refresh_token(token)
        token_type = payload.get('type')
        if token_type != 'refresh':
            raise TokenTypeException()
        user_id = int(payload.get('sub'))
        db_user = await self.__user_repository.find_by_id(user_id)
        if db_user is None:
            raise UserNotFoundException()
        access_token = create_token(token_data = {'sub': str(user_id)}, expires_time_minutes = 30, token_type = 'access')
        return TokenSchema(access_token = access_token)
        