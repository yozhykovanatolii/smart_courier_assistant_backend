from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import get_auth_service, get_otp_service
from clients.mail_client import send_verification_letter
from schemas.otp_code import ResendOtpSchema, VerifyEmailSchema
from schemas.token import TokenSchema
from schemas.user import UserRegisterSchema, UserLoginSchema
from services.auth_service import AuthService
from services.otp_service import OtpService

auth_router = APIRouter(prefix='/auth')
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
OtpServiceDependency = Annotated[OtpService, Depends(get_otp_service)]

@auth_router.post('/register', status_code = status.HTTP_201_CREATED)
async def register_user(user_register: UserRegisterSchema, auth_service: AuthServiceDependency, otp_service: OtpServiceDependency):
    await auth_service.register_user(user_register)
    otp_code = await otp_service.create_otp(user_register.email)
    await send_verification_letter(user_register.email, otp_code)
    return {'message': 'Success registration. Verification code has been sent to your email'}
    
@auth_router.post('/login', status_code = status.HTTP_200_OK)
async def login_user(user_login: UserLoginSchema, auth_service: AuthServiceDependency):
    return await auth_service.login_user(user_login)

@auth_router.post('/verify-email', status_code = status.HTTP_200_OK)
async def verify_email(verify_email_schema: VerifyEmailSchema, otp_service: OtpServiceDependency):
    await otp_service.verify_otp(verify_email_schema.email, verify_email_schema.code)
    return {'message': 'Email verified successfully'}

@auth_router.post('/resend-code', status_code = status.HTTP_200_OK)
async def resend_code(resend_otp_schema: ResendOtpSchema, otp_service: OtpServiceDependency):
    otp_code = await otp_service.resend_otp(resend_otp_schema.email)
    await send_verification_letter(resend_otp_schema.email, otp_code)
    return {'message': 'Verification code has been resent'}

@auth_router.post('/refresh', status_code = status.HTTP_200_OK, response_model = TokenSchema, response_model_exclude_none = True)
async def refresh_token(token: str | None, auth_service: AuthServiceDependency):
    return await auth_service.refresh_token(token)