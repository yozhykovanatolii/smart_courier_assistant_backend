from exceptions.app_exception import AppException


class ExternalServiceException(AppException):
    pass
      
class ChatGptAnalysisException(ExternalServiceException):
    def __init__(self):
        super().__init__(
            message="Failed to analyze the route using ChatGPT",
            error_code="chatgpt_analysis_failed",
        )
        
class OptimizationRouteException(ExternalServiceException):
    def __init__(self):
        super().__init__(
            message="Failed to optimize the route",
            error_code="route_optimization_failed",
        )