"""Authentication helper for login/token management."""

from __future__ import annotations

from typing import Any

from loguru import logger

from config.config import config
from utils.request_util import request_util


class AuthUtil:
    def __init__(self) -> None:
        self.token: str | None = None
        self.user_info: dict[str, Any] | None = None

    def login(self, username: str, password: str) -> dict[str, Any] | None:
        payload = {"account": username, "password": password}
        logger.info("login attempt for {}", username)

        try:
            response = request_util.post("/api/user/login", json=payload)
            result = response.json()
        except Exception as exc:
            logger.error("login request failed: {}", exc)
            return None

        logger.info("login response: {}", result)
        if result.get("code") != 200:
            logger.error("login failed: {}", result.get("message", "unknown error"))
            return None

        data = result.get("data") or {}
        token = data.get("token") or result.get("token")
        if not token:
            logger.error("login succeeded but token is missing")
            return None

        self.token = token
        self.user_info = data.get("user")
        request_util.set_token(token)
        return data

    def admin_login(self, username: str | None = None, password: str | None = None) -> dict[str, Any] | None:
        return self.login(username or config.admin_username, password or config.admin_password)

    def user_login(self, username: str | None = None, password: str | None = None) -> dict[str, Any] | None:
        return self.login(username or config.test_user_username, password or config.test_user_password)

    def logout(self) -> None:
        self.token = None
        self.user_info = None
        request_util.clear_token()

    def get_token(self) -> str | None:
        return self.token

    def get_user_info(self) -> dict[str, Any] | None:
        return self.user_info

    def is_admin(self) -> bool:
        if not self.user_info:
            return False
        role = self.user_info.get("role")
        return role == 2 or role == "admin" or role == "ADMIN"

    def ensure_login(self, user_type: str = "user") -> str | None:
        if self.token:
            return self.token
        result = self.admin_login() if user_type == "admin" else self.user_login()
        return self.token if result else None


auth_util = AuthUtil()
