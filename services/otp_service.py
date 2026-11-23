from exceptions.authentication_exception import UserNotFoundException
from exceptions.bad_request_exception import EmailAlreadyVerifiedException, InvalidOtpException
from repositories.otp_repository import OtpRepository
from repositories.user_repository import UserRepository
from security import hash_email, generate_code, verify_otp_code

class OtpService:
    def __init__(self, otp_repository: OtpRepository, user_repository: UserRepository):
        self.__otp_repository = otp_repository
        self.__user_repository = user_repository
        
    def __build_key(self, email: str) -> str:
        email_hash = hash_email(email)
        return f"otp:register:{email_hash}"
        
    async def create_otp(self, email: str) -> str:
        key = self.__build_key(email)
        code = generate_code()
        await self.__otp_repository.save_opt_code(key=key, code=code)
        return code
    
    async def verify_otp(self, email: str, input_code: str) -> None:
        key = self.__build_key(email)
        stored_code = await self.__otp_repository.consume_opt_code(key)
        if stored_code is None or not verify_otp_code(stored_code, input_code):
            raise InvalidOtpException()
        await self.__user_repository.update_user_verification_status(email)
    
    async def resend_otp(self, email: str) -> str:
        normalized_email = email.strip().lower()
        user = await self.__user_repository.get_user_by_email(normalized_email)
        if user is None:
            raise UserNotFoundException()
        if user.is_verified:
            raise EmailAlreadyVerifiedException()
        return await self.create_otp(normalized_email)
    
    