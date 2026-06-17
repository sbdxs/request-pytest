"""User API wrappers."""

from __future__ import annotations

from api.base_api import BaseAPI


class UserAPI(BaseAPI):
    def register(
        self,
        username: str,
        password: str,
        email: str,
        nickname: str | None = None,
        student_id: str | None = None,
        phone: str | None = None,
    ) -> dict:
        payload = {
            "username": username,
            "password": password,
            "email": email,
        }
        if nickname:
            payload["nickname"] = nickname
        if student_id:
            payload["studentId"] = student_id
        if phone:
            payload["phone"] = phone
        return self._post("/api/user/register", json=payload)

    def login(self, username: str, password: str) -> dict:
        return self._post("/api/user/login", json={"account": username, "password": password})

    def get_current_user(self) -> dict:
        return self._get("/api/user/info")

    def get_ban_status(self) -> dict:
        return self._get("/api/user/ban-status")

    def update_profile(
        self,
        nickname: str | None = None,
        real_name: str | None = None,
        college: str | None = None,
        avatar: str | None = None,
        phone: str | None = None,
        email: str | None = None,
    ) -> dict:
        payload = {}
        if nickname is not None:
            payload["nickname"] = nickname
        if real_name is not None:
            payload["realName"] = real_name
        if college is not None:
            payload["college"] = college
        if avatar is not None:
            payload["avatar"] = avatar
        if phone is not None:
            payload["phone"] = phone
        if email is not None:
            payload["email"] = email
        return self._put("/api/user/profile", json=payload)

    def change_password(self, old_password: str, new_password: str) -> dict:
        return self._post(
            "/api/user/password",
            json={"oldPassword": old_password, "newPassword": new_password},
        )

    def get_dashboard(self) -> dict:
        return self._get("/api/user/admin/dashboard")

    def get_users(
        self,
        page_num: int = 1,
        page_size: int = 10,
        keyword: str | None = None,
        status: int | None = None,
        role: int | None = None,
    ) -> dict:
        params = {"pageNum": page_num, "pageSize": page_size}
        if keyword:
            params["keyword"] = keyword
        if status is not None:
            params["status"] = status
        if role is not None:
            params["role"] = role
        return self._get("/api/user/admin/list", params=params)

    def ban_user(self, user_id: int, ban_type: int, reason: str, expires_at: str | None = None) -> dict:
        payload = {"banType": ban_type, "reason": reason}
        if expires_at:
            payload["banExpiresAt"] = expires_at
        return self._post(f"/api/user/admin/{user_id}/ban", json=payload)

    def unban_user(self, user_id: int) -> dict:
        return self._post(f"/api/user/admin/{user_id}/unban")


user_api = UserAPI()
