"""User API wrappers."""

from __future__ import annotations

from api.base_api import BaseAPI


class UserAPI(BaseAPI):
    def register(
        self,
        username: str,
        password: str,
        email: str | None = None,
        nickname: str | None = None,
        student_id: str | None = None,
        phone: str | None = None,
    ) -> dict:
        """对应 POST /api/user/register（用户注册）"""
        payload = {
            "username": username,
            "password": password,
        }
        if email:
            payload["email"] = email
        if nickname:
            payload["nickname"] = nickname
        if student_id:
            payload["studentId"] = student_id
        if phone:
            payload["phone"] = phone
        return self._post("/api/user/register", json=payload)

    def login(self, username: str, password: str) -> dict:
        """对应 POST /api/user/login（用户登录）"""
        return self._post("/api/user/login", json={"account": username, "password": password})

    def get_current_user(self) -> dict:
        """对应 GET /api/user/info（获取当前用户信息）"""
        return self._get("/api/user/info")

    def get_ban_status(self) -> dict:
        """对应 GET /api/user/ban-status（查询封禁状态）"""
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
        """对应 PUT /api/user/profile（修改个人资料）"""
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
        """对应 POST /api/user/password（修改密码）"""
        return self._post(
            "/api/user/password",
            json={"oldPassword": old_password, "newPassword": new_password},
        )

    def get_dashboard(self) -> dict:
        """对应 GET /api/user/admin/dashboard（后台数据看板）"""
        return self._get("/api/user/admin/dashboard")

    def get_users(
        self,
        page_num: int = 1,
        page_size: int = 10,
        keyword: str | None = None,
        status: int | None = None,
        role: int | None = None,
    ) -> dict:
        """对应 GET /api/user/admin/list（分页查询用户列表）"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if keyword:
            params["keyword"] = keyword
        if status is not None:
            params["status"] = status
        if role is not None:
            params["role"] = role
        return self._get("/api/user/admin/list", params=params)

    def ban_user(self, user_id: int, ban_type: int, reason: str, expires_at: str | None = None) -> dict:
        """对应 POST /api/user/admin/{user_id}/ban（封禁用户）"""
        payload = {"banType": ban_type, "reason": reason}
        if expires_at:
            payload["banExpiresAt"] = expires_at
        return self._post(f"/api/user/admin/{user_id}/ban", json=payload)

    def unban_user(self, user_id: int) -> dict:
        """对应 POST /api/user/admin/{user_id}/unban（解除封禁）"""
        return self._post(f"/api/user/admin/{user_id}/unban")

    def admin_get_user_detail(self, user_id: int) -> dict:
        """对应 GET /api/user/admin/{user_id}/detail（查询用户详情）"""
        return self._get(f"/api/user/admin/{user_id}/detail")

    def admin_update_user(self, user_id: int, nickname: str | None = None, email: str | None = None) -> dict:
        """对应 PUT /api/user/admin/{user_id}（管理员修改用户）"""
        payload: dict[str, object] = {}
        if nickname is not None:
            payload["nickname"] = nickname
        if email is not None:
            payload["email"] = email
        return self._put(f"/api/user/admin/{user_id}", json=payload)

    def upload_avatar(self, file_path: str) -> dict:
        """对应 POST /api/user/upload/avatar（上传头像）"""
        return self._post_files("/api/user/upload/avatar", file_field="file", file_paths=[file_path])

    def upload_news_image(self, file_path: str) -> dict:
        """对应 POST /api/user/upload/news（上传资讯图片）"""
        return self._post_files("/api/user/upload/news", file_field="file", file_paths=[file_path])

    def upload_lost_found_image(self, file_path: str) -> dict:
        """对应 POST /api/user/upload/lost-found（上传失物图片）"""
        return self._post_files("/api/user/upload/lost-found", file_field="file", file_paths=[file_path])

    def upload_lost_found_multiple(self, file_paths: list[str]) -> dict:
        """对应 POST /api/user/upload/lost-found/multiple（批量上传失物图片）"""
        return self._post_files("/api/user/upload/lost-found/multiple", file_field="files", file_paths=file_paths)

    def upload_forum_multiple(self, file_paths: list[str]) -> dict:
        """对应 POST /api/user/upload/forum/multiple（批量上传帖子图片）"""
        return self._post_files("/api/user/upload/forum/multiple", file_field="files", file_paths=file_paths)


user_api = UserAPI()
