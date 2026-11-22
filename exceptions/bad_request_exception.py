from exceptions.app_exception import AppException


class BadRequestException(AppException):
    pass


class InvalidOtpException(BadRequestException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired OTP code",
            error_code="invalid_otp_code",
        )


class EmailAlreadyVerifiedException(BadRequestException):
    def __init__(self):
        super().__init__(
            message="Email is already verified",
            error_code="email_already_verified",
        )
