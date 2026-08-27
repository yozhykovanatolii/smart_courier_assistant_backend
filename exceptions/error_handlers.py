from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from exceptions.access_denied_exception import AccessDeniedException
from exceptions.authentication_exception import AuthenticationException
from exceptions.email_already_used_exception import EmailAlreadyUsedException
from exceptions.external_service_exception import ExternalServiceException
from exceptions.resource_not_found_exception import ResourceNotFoundException

def register_error_handlers(app: FastAPI):
    @app.exception_handler(AuthenticationException)
    def authentication_exception_handler(_: Request, exception: AuthenticationException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(AccessDeniedException)
    def access_denied_exception_handler(_: Request, exception: AccessDeniedException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(EmailAlreadyUsedException)
    def email_already_use_exception_handler(_: Request, exception: EmailAlreadyUsedException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(ResourceNotFoundException)
    def resource_not_found_exception_handler(_: Request, exception: ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(ExternalServiceException)
    def external_service_exception_handler(_: Request, exception: ExternalServiceException):
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                'error_code': exception.error_code,
                'message': exception.message,
            }
        )
        
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(_: Request, exception: RequestValidationError):
        messages = [error["msg"] for error in exception.errors()]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                'error_code': 'validation_error',
                'message': '; '.join(messages),
            }
        )