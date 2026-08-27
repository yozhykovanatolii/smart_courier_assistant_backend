from exceptions.app_exception import AppException


class ResourceNotFoundException(AppException):
    pass


class OrderNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(
            message="Order was not found",
            error_code="order_not_found",
        )
        
class RouteNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(
            message="Route was not found",
            error_code="route_not_found",
        )