"""
API模块初始化
"""
from .base_api import BaseAPI
from .user_api import user_api, UserAPI
from .lostfound_api import lostfound_api, LostFoundAPI
from .forum_api import forum_api, ForumAPI
from .im_api import im_api, ImAPI
from .news_api import news_api, NewsAPI
from .home_api import home_api, HomeAPI

__all__ = [
    "BaseAPI",
    "user_api", "UserAPI",
    "lostfound_api", "LostFoundAPI",
    "forum_api", "ForumAPI",
    "im_api", "ImAPI",
    "news_api", "NewsAPI",
    "home_api", "HomeAPI"
]