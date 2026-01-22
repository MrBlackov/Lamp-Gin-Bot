from app.exeption.base import BotError

class ApiError(BotError):
    msg = ''

class ValidationApiError(ApiError):
    msg = ''