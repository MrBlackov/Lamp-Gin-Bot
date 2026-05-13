from app.aio.cls.callback.base import BaseCall, MenuCall
from typing import Any, Literal

class SocialBackCall(BaseCall, prefix='social_back'):
    where: str

class SocialActionCall(BaseCall, prefix='social_action'):
    to_send_request: bool = False

class SocialFriendCall(BaseCall, prefix='social_friend'):
    to_delete: bool = False
    to_info: bool = False
    user_id: int

class SocialRequestCall(BaseCall, prefix='social_request'):
    status: str
    user_id: int
