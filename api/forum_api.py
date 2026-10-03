"""Forum API wrappers."""

from __future__ import annotations

from api.base_api import BaseAPI


class ForumAPI(BaseAPI):
    def get_categories(self) -> dict:
        """对应 GET /api/forum/categories（获取帖子分类）"""
        return self._get("/api/forum/categories")

    def create_post(
        self,
        title: str,
        content: str,
        category_id: int | None = None,
        cover_images: str | None = None,
    ) -> dict:
        """对应 POST /api/forum/posts（发布帖子）"""
        payload = {
            "title": title,
            "content": content,
        }
        if category_id is not None:
            payload["categoryId"] = category_id
        if cover_images is not None:
            payload["coverImages"] = cover_images
        return self._post("/api/forum/posts", json=payload)

    def list_posts(
        self,
        page_num: int = 1,
        page_size: int = 10,
        category_id: int | None = None,
        keyword: str | None = None,
        sort_by: str | None = None,
    ) -> dict:
        """对应 GET /api/forum/posts（分页查询帖子）"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if category_id is not None:
            params["categoryId"] = category_id
        if keyword:
            params["keyword"] = keyword
        if sort_by:
            params["sortBy"] = sort_by
        return self._get("/api/forum/posts", params=params)

    def get_post_detail(self, post_id: int) -> dict:
        """对应 GET /api/forum/posts/{post_id}（查询帖子详情）"""
        return self._get(f"/api/forum/posts/{post_id}")

    def delete_post(self, post_id: int) -> dict:
        """对应 DELETE /api/forum/posts/{post_id}（删除帖子）"""
        return self._delete(f"/api/forum/posts/{post_id}")

    def list_my_published(self, page_num: int = 1, page_size: int = 10) -> dict:
        """对应 GET /api/forum/posts/my/published（查询我发布的帖子）"""
        return self._get(
            "/api/forum/posts/my/published",
            params={"pageNum": page_num, "pageSize": page_size},
        )

    def list_my_replied(self, page_num: int = 1, page_size: int = 10) -> dict:
        """对应 GET /api/forum/posts/my/replied（查询我回复的帖子）"""
        return self._get(
            "/api/forum/posts/my/replied",
            params={"pageNum": page_num, "pageSize": page_size},
        )

    def list_my_favorited(self, page_num: int = 1, page_size: int = 10) -> dict:
        """对应 GET /api/forum/posts/my/favorited（查询我收藏的帖子）"""
        return self._get(
            "/api/forum/posts/my/favorited",
            params={"pageNum": page_num, "pageSize": page_size},
        )

    def create_comment(self, post_id: int, content: str, reply_to: int | None = None) -> dict:
        """对应 POST /api/forum/posts/{post_id}/comments（发表评论）"""
        payload = {"content": content}
        if reply_to is not None:
            payload["replyTo"] = reply_to
        return self._post(f"/api/forum/posts/{post_id}/comments", json=payload)

    def list_comments(self, post_id: int, page_num: int = 1, page_size: int = 10) -> dict:
        """对应 GET /api/forum/posts/{post_id}/comments（分页查询评论）"""
        return self._get(
            f"/api/forum/posts/{post_id}/comments",
            params={"pageNum": page_num, "pageSize": page_size},
        )

    def delete_comment(self, comment_id: int) -> dict:
        """对应 DELETE /api/forum/comments/{comment_id}（删除评论）"""
        return self._delete(f"/api/forum/comments/{comment_id}")

    def like_post(self, post_id: int) -> dict:
        """对应 POST /api/forum/posts/{post_id}/like（点赞帖子）"""
        return self._post(f"/api/forum/posts/{post_id}/like")

    def unlike_post(self, post_id: int) -> dict:
        """对应 DELETE /api/forum/posts/{post_id}/like（取消点赞）"""
        return self._delete(f"/api/forum/posts/{post_id}/like")

    def favorite_post(self, post_id: int) -> dict:
        """对应 POST /api/forum/posts/{post_id}/favorite（收藏帖子）"""
        return self._post(f"/api/forum/posts/{post_id}/favorite")

    def unfavorite_post(self, post_id: int) -> dict:
        """对应 DELETE /api/forum/posts/{post_id}/favorite（取消收藏）"""
        return self._delete(f"/api/forum/posts/{post_id}/favorite")

    def report_post(self, post_id: int, reason_type: int, reason_text: str | None = None) -> dict:
        """对应 POST /api/forum/posts/{post_id}/report（举报帖子）"""
        payload = {"reasonType": reason_type}
        if reason_text:
            payload["reasonText"] = reason_text
        return self._post(f"/api/forum/posts/{post_id}/report", json=payload)

    def admin_list_pending(self, page_num: int = 1, page_size: int = 10) -> dict:
        """对应 GET /api/forum/admin/posts/pending（查询待审核帖子）"""
        return self._get(
            "/api/forum/admin/posts/pending",
            params={"pageNum": page_num, "pageSize": page_size},
        )

    def admin_list_moderation(
        self,
        page_num: int = 1,
        page_size: int = 10,
        category_id: int | None = None,
        moderation_status: int | None = None,
    ) -> dict:
        """对应 GET /api/forum/admin/posts/moderation（分页查询审核列表）"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if category_id is not None:
            params["categoryId"] = category_id
        if moderation_status is not None:
            params["moderationStatus"] = moderation_status
        return self._get("/api/forum/admin/posts/moderation", params=params)

    def admin_list_comments(
        self,
        page_num: int = 1,
        page_size: int = 10,
        keyword: str | None = None,
    ) -> dict:
        """对应 GET /api/forum/admin/comments（分页查询评论列表）"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if keyword:
            params["keyword"] = keyword
        return self._get("/api/forum/admin/comments", params=params)

    def admin_list_reports(self, page_num: int = 1, page_size: int = 10, status: int | None = None) -> dict:
        """对应 GET /api/forum/admin/reports（分页查询举报列表）"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        return self._get("/api/forum/admin/reports", params=params)

    def admin_audit_post(
        self,
        post_id: int,
        audit_status: int,
        audit_remark: str | None = None,
    ) -> dict:
        """对应 PATCH /api/forum/admin/posts/{post_id}/audit（审核帖子）"""
        payload = {"auditStatus": audit_status}
        if audit_remark:
            payload["auditRemark"] = audit_remark
        return self._patch(f"/api/forum/admin/posts/{post_id}/audit", json=payload)

    def admin_update_moderation(
        self,
        post_id: int,
        moderation_status: int,
        remark: str | None = None,
    ) -> dict:
        """对应 PATCH /api/forum/admin/posts/{post_id}/moderation（更新风控状态）"""
        payload = {"moderationStatus": moderation_status}
        if remark:
            payload["remark"] = remark
        return self._patch(f"/api/forum/admin/posts/{post_id}/moderation", json=payload)

    def admin_audit_report(
        self,
        report_id: int,
        status: int,
        handle_remark: str | None = None,
    ) -> dict:
        """对应 PATCH /api/forum/admin/reports/{report_id}（处理举报）"""
        payload = {"status": status}
        if handle_remark:
            payload["handleRemark"] = handle_remark
        return self._patch(f"/api/forum/admin/reports/{report_id}", json=payload)


forum_api = ForumAPI()
