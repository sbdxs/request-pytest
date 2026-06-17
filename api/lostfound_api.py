"""Lost and found API wrappers."""

from __future__ import annotations

from api.base_api import BaseAPI


class LostFoundAPI(BaseAPI):
    def create(
        self,
        item_type: int,
        title: str,
        item_name: str,
        category: int,
        description: str | None = None,
        location_area: str | None = None,
        location_detail: str | None = None,
        event_time: str | None = None,
        images: str | None = None,
        contact_way: int | None = None,
        is_contact_public: int | None = None,
    ) -> dict:
        payload = {
            "type": item_type,
            "title": title,
            "itemName": item_name,
            "category": category,
        }
        if description is not None:
            payload["description"] = description
        if location_area is not None:
            payload["locationArea"] = location_area
        if location_detail is not None:
            payload["locationDetail"] = location_detail
        if event_time is not None:
            payload["eventTime"] = event_time
        if images is not None:
            payload["images"] = images
        if contact_way is not None:
            payload["contactWay"] = contact_way
        if is_contact_public is not None:
            payload["isContactPublic"] = is_contact_public
        return self._post("/api/lost-found", json=payload)

    def list(
        self,
        page_num: int = 1,
        page_size: int = 10,
        item_type: int | None = None,
        category: int | None = None,
        area: str | None = None,
        keyword: str | None = None,
        sort_by: str | None = None,
        status: int | None = None,
    ) -> dict:
        params = {"pageNum": page_num, "pageSize": page_size}
        if item_type is not None:
            params["type"] = item_type
        if category is not None:
            params["category"] = category
        if area:
            params["area"] = area
        if keyword:
            params["keyword"] = keyword
        if sort_by:
            params["sortBy"] = sort_by
        if status is not None:
            params["status"] = status
        return self._get("/api/lost-found", params=params)

    def get_detail(self, lost_found_id: int) -> dict:
        return self._get(f"/api/lost-found/{lost_found_id}")

    def update_status(self, lost_found_id: int, status: int) -> dict:
        return self._patch(f"/api/lost-found/{lost_found_id}/status", json={"status": status})

    def delete(self, lost_found_id: int) -> dict:
        return self._delete(f"/api/lost-found/{lost_found_id}")

    def list_my(self, page_num: int = 1, page_size: int = 10, status: int | None = None) -> dict:
        params = {"pageNum": page_num, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        return self._get("/api/lost-found/my", params=params)

    def update(
        self,
        lost_found_id: int,
        item_type: int | None = None,
        title: str | None = None,
        item_name: str | None = None,
        category: int | None = None,
        description: str | None = None,
        location_area: str | None = None,
        location_detail: str | None = None,
        event_time: str | None = None,
        images: str | None = None,
        contact_way: int | None = None,
        is_contact_public: int | None = None,
    ) -> dict:
        payload: dict[str, object] = {}
        if item_type is not None:
            payload["type"] = item_type
        if title is not None:
            payload["title"] = title
        if item_name is not None:
            payload["itemName"] = item_name
        if category is not None:
            payload["category"] = category
        if description is not None:
            payload["description"] = description
        if location_area is not None:
            payload["locationArea"] = location_area
        if location_detail is not None:
            payload["locationDetail"] = location_detail
        if event_time is not None:
            payload["eventTime"] = event_time
        if images is not None:
            payload["images"] = images
        if contact_way is not None:
            payload["contactWay"] = contact_way
        if is_contact_public is not None:
            payload["isContactPublic"] = is_contact_public
        return self._put(f"/api/lost-found/{lost_found_id}", json=payload)

    def report(self, lost_found_id: int, reason: str) -> dict:
        return self._post(
            "/api/lost-found/report",
            json={"lostFoundId": lost_found_id, "reason": reason},
        )

    def admin_delete(self, lost_found_id: int, delete_reason: str) -> dict:
        return self._delete(
            f"/api/lost-found/admin/{lost_found_id}",
            params={"deleteReason": delete_reason},
        )

    def admin_list(
        self,
        page_num: int = 1,
        page_size: int = 10,
        status: int | None = None,
        moderation_status: int | None = None,
        keyword: str | None = None,
    ) -> dict:
        params = {"pageNum": page_num, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        if moderation_status is not None:
            params["moderationStatus"] = moderation_status
        if keyword:
            params["keyword"] = keyword
        return self._get("/api/lost-found/admin/list", params=params)

    def admin_get_detail(self, lost_found_id: int) -> dict:
        return self._get(f"/api/lost-found/admin/{lost_found_id}")

    def admin_get_reports(self, lost_found_id: int) -> dict:
        return self._get(f"/api/lost-found/admin/{lost_found_id}/reports")

    def admin_audit(
        self,
        lost_found_id: int,
        audit_status: int,
        audit_remark: str | None = None,
    ) -> dict:
        payload = {"auditStatus": audit_status}
        if audit_remark:
            payload["auditRemark"] = audit_remark
        return self._patch(f"/api/lost-found/admin/{lost_found_id}/audit", json=payload)

    def admin_update_moderation(
        self,
        lost_found_id: int,
        moderation_status: int,
        remark: str | None = None,
    ) -> dict:
        payload = {"moderationStatus": moderation_status}
        if remark:
            payload["remark"] = remark
        return self._patch(f"/api/lost-found/admin/{lost_found_id}/moderation", json=payload)

    def admin_report_list(self, page_num: int = 1, page_size: int = 10, status: int | None = None) -> dict:
        params = {"pageNum": page_num, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        return self._get("/api/lost-found/admin/reports", params=params)

    def admin_audit_report(
        self,
        report_id: int,
        status: int,
        handle_remark: str | None = None,
    ) -> dict:
        payload = {"status": status}
        if handle_remark:
            payload["handleRemark"] = handle_remark
        return self._patch(f"/api/lost-found/admin/reports/{report_id}", json=payload)


lostfound_api = LostFoundAPI()
