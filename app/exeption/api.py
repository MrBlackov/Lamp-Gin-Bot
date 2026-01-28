from app.exeption.base import BotError

class ApiError(BotError):
    pass
class ValidationApiError(ApiError):
    pass