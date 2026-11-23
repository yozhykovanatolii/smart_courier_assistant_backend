from exceptions.app_exception import AppException


class AccessDeniedException(AppException):
    def __init__(
        self,
        message: str = "Access was denied",
        error_code: str = "access_denied",
    ):
        super().__init__(
            message=message,
            error_code=error_code,
        )
        
class EmailNotVerifiedException(AccessDeniedException):
    def __init__(self):
        super().__init__(
            message="Email is not verified",
            error_code="email_not_verified",
        )