"""IM API wrappers."""

from __future__ import annotations

from api.base_api import BaseAPI


class ImAPI(BaseAPI):
    def create_conversation(
        self,
        target_user_id: int,
        biz_type: int | None = None,
        biz_id: int | None = None,
    ) -> dict:
        """对应 POST /api/im/conversations（创建会话）"""
        payload = {"targetUserId": target_user_id}
        if biz_type is not None:
            payload["bizType"] = biz_type
        if biz_id is not None:
            payload["bizId"] = biz_id
        return self._post("/api/im/conversations", json=payload)

    def list_conversations(self) -> dict:
        """对应 GET /api/im/conversations（查询会话列表）"""
        return self._get("/api/im/conversations")

    def list_messages(self, conversation_id: int, page_num: int = 1, page_size: int = 20) -> dict:
        """对应 GET /api/im/conversations/{conversation_id}/messages（分页查询消息）"""
        return self._get(
            f"/api/im/conversations/{conversation_id}/messages",
            params={"pageNum": page_num, "pageSize": page_size},
        )

    def send_message(self, conversation_id: int, content: str, message_type: int = 1) -> dict:
        """对应 POST /api/im/conversations/{conversation_id}/messages（发送消息）"""
        return self._post(
            f"/api/im/conversations/{conversation_id}/messages",
            json={"content": content, "type": message_type},
        )

    def report_message(self, message_id: int, reason: str, reason_type: int = 0) -> dict:
        """对应 POST /api/im/messages/{message_id}/report（举报消息）"""
        return self._post(
            f"/api/im/messages/{message_id}/report",
            json={"reasonText": reason, "reasonType": reason_type},
        )

    def mark_read(self, conversation_id: int) -> dict:
        """对应 POST /api/im/conversations/{conversation_id}/read（标记已读）"""
        return self._post(f"/api/im/conversations/{conversation_id}/read")

    def get_unread_count(self) -> dict:
        """对应 GET /api/im/unread-count（查询未读数）"""
        return self._get("/api/im/unread-count")

    def admin_list_reports(self, page_num: int = 1, page_size: int = 10, status: int | None = None) -> dict:
        """对应 GET /api/im/admin/reports（分页查询举报列表）"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        return self._get("/api/im/admin/reports", params=params)

    def admin_audit_report(
        self,
        report_id: int,
        status: int,
        ban_type: int | None = None,
        ban_days: int | None = None,
        handle_remark: str | None = None,
    ) -> dict:
        """对应 PATCH /api/im/admin/reports/{report_id}（处理举报）"""
        payload = {"status": status}
        if ban_type is not None:
            payload["banType"] = ban_type
        if ban_days is not None:
            payload["banDays"] = ban_days
        if handle_remark is not None:
            payload["handleRemark"] = handle_remark
        return self._patch(f"/api/im/admin/reports/{report_id}", json=payload)


im_api = ImAPI()
