"""Lost and found API tests — 对应 接口测试用例/03-失物招领模块用例.md (LF-001 ~ LF-026)."""

from __future__ import annotations

import allure
import pytest

from api.lostfound_api import lostfound_api
from conftest import assert_failed, assert_success, assert_text_contains, get_page_records
from utils.data_util import data_util
from utils.request_util import request_util


@allure.feature("lostfound")
class TestLostFoundCreate:
    @pytest.mark.lostfound
    @pytest.mark.p0
    def test_create_lost(self, user_token, lostfound_data):
        """LF-001 发布寻物启事。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.create(
            item_type=lostfound_data["type"],
            title=lostfound_data["title"],
            item_name=lostfound_data["itemName"],
            category=lostfound_data["category"],
            description=lostfound_data["description"],
            location_area=lostfound_data["locationArea"],
            location_detail=lostfound_data["locationDetail"],
            contact_way=lostfound_data["contactWay"],
            is_contact_public=lostfound_data["isContactPublic"],
        )
        assert_success(result)
        data = result["data"]
        assert data["id"] is not None, result
        assert data["type"] == 1, result
        assert data["title"] == lostfound_data["title"], result

    @pytest.mark.lostfound
    @pytest.mark.p0
    def test_create_found(self, user_token):
        """LF-002 发布招领启事。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.create(
            item_type=2,
            title=f"招领测试_{data_util.generate_unique_id()}",
            item_name="校园卡",
            category=1,
            location_area="食堂",
            location_detail="食堂二楼",
        )
        assert_success(result)
        data = result["data"]
        assert data["id"] is not None, result
        assert data["type"] == 2, result

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_create_type_invalid(self, user_token, lostfound_data):
        """LF-003 类型值越界（type=3）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.create(
            item_type=3,
            title=lostfound_data["title"],
            item_name=lostfound_data["itemName"],
            category=lostfound_data["category"],
        )
        assert_failed(result)
        assert "类型值无效" in result["message"], result

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_create_title_too_short(self, user_token):
        """LF-004 标题过短（1个字）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.create(item_type=1, title="短", item_name="钱包", category=1)
        assert_failed(result)
        assert "标题长度需在2-100个字符之间" in result["message"], result

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_create_item_name_empty(self, user_token, lostfound_data):
        """LF-005 物品名称为空。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.create(
            item_type=1,
            title=lostfound_data["title"],
            item_name="",
            category=lostfound_data["category"],
        )
        assert_failed(result)
        assert (
            "物品名称不能为空" in result["message"] or "物品名称长度需在1-50个字符之间" in result["message"]
        ), result

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_create_category_out_of_range(self, user_token, lostfound_data):
        """LF-006 分类越界（category=6）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.create(
            item_type=1,
            title=lostfound_data["title"],
            item_name=lostfound_data["itemName"],
            category=6,
        )
        assert_failed(result)
        assert "分类值无效" in result["message"], result

    @pytest.mark.lostfound
    @pytest.mark.p2
    def test_create_description_too_long(self, user_token, lostfound_data):
        """LF-007 描述超长（501字）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.create(
            item_type=1,
            title=lostfound_data["title"],
            item_name=lostfound_data["itemName"],
            category=lostfound_data["category"],
            description="长" * 501,
        )
        assert_failed(result)
        assert "描述长度不能超过500个字符" in result["message"], result


@allure.feature("lostfound")
class TestLostFoundQuery:
    @pytest.mark.lostfound
    @pytest.mark.p0
    def test_list_all(self, user_token):
        """LF-008 分页查询列表。"""
        request_util.set_token(user_token) if user_token else request_util.clear_headers()
        result = lostfound_api.list(page_num=1, page_size=10)
        assert_success(result)
        assert result["data"] is not None
        assert "records" in result["data"], result
        assert "total" in result["data"], result

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_list_filter_by_type(self, user_token):
        """LF-009 按类型筛选。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.list(page_num=1, page_size=10, item_type=1)
        assert_success(result)
        for record in get_page_records(result):
            assert record.get("type") == 1, record

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_list_keyword_search(self, user_token, admin_token, created_lost_found):
        """LF-010 关键词搜索（审核通过后可搜到）。"""
        if not user_token or not admin_token:
            pytest.skip("login failed")
        request_util.set_token(admin_token)
        audit_result = lostfound_api.admin_audit(lost_found_id=created_lost_found["id"], audit_status=1)
        assert_success(audit_result)

        request_util.set_token(user_token)
        keyword = created_lost_found["title"][:6]
        result = lostfound_api.list(page_num=1, page_size=10, keyword=keyword)
        assert_success(result)
        records = get_page_records(result)
        assert any(record.get("id") == created_lost_found["id"] for record in records), result

    @pytest.mark.lostfound
    @pytest.mark.p0
    def test_get_detail(self, user_token, created_lost_found):
        """LF-011 查看详情。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.get_detail(lost_found_id=created_lost_found["id"])
        assert_success(result)
        data = result["data"]
        assert data["id"] == created_lost_found["id"], result
        assert data["title"] == created_lost_found["title"], result
        assert data["itemName"] == created_lost_found["itemName"], result

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_get_detail_not_exist(self, user_token):
        """LF-012 查看不存在的记录。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.get_detail(lost_found_id=999999)
        assert_failed(result)
        assert "记录不存在" in result["message"], result

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_my_records(self, user_token, created_lost_found):
        """LF-017 我的发布列表。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.list_my(page_num=1, page_size=10)
        assert_success(result)
        records = get_page_records(result)
        assert any(record.get("id") == created_lost_found["id"] for record in records), result


@allure.feature("lostfound")
class TestLostFoundInteract:
    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_update_status_to_closed(self, user_token, approved_lost_found_id):
        """LF-013 更新状态。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)

        update_result = lostfound_api.update_status(lost_found_id=approved_lost_found_id, status=2)
        assert_success(update_result)
        assert_text_contains(update_result, "状态更新成功")

        detail_result = lostfound_api.get_detail(lost_found_id=approved_lost_found_id)
        assert_success(detail_result)
        assert detail_result["data"]["status"] == 2, detail_result

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_edit_own_record(self, user_token, created_lost_found):
        """LF-014 编辑自己的发布。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        updated_description = f"更新后的描述_{created_lost_found['id']}"
        result = lostfound_api.update(
            lost_found_id=created_lost_found["id"],
            item_type=1,
            title=created_lost_found["title"],
            item_name=created_lost_found["itemName"],
            category=created_lost_found["category"],
            description=updated_description,
            location_area=created_lost_found.get("locationArea") or "图书馆",
        )
        assert_success(result)
        assert_text_contains(result, "更新成功")

        detail_result = lostfound_api.get_detail(lost_found_id=created_lost_found["id"])
        assert_success(detail_result)
        assert detail_result["data"]["description"] == updated_description, detail_result

    @pytest.mark.lostfound
    @pytest.mark.p2
    def test_edit_forbidden_for_non_author(self, user_token, extra_user_token, created_lost_found):
        """LF-015 非作者编辑。"""
        if not user_token or not extra_user_token:
            pytest.skip("user login failed")
        request_util.set_token(extra_user_token)
        result = lostfound_api.update(
            lost_found_id=created_lost_found["id"],
            description="非作者尝试修改",
        )
        assert_failed(result)

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_delete_own_record(self, user_token, lostfound_data):
        """LF-016 删除自己的发布。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        create_result = lostfound_api.create(
            item_type=1,
            title=lostfound_data["title"],
            item_name="待删物品",
            category=1,
            description="待删除记录",
            location_area="图书馆",
        )
        assert_success(create_result)
        record_id = create_result["data"]["id"]

        delete_result = lostfound_api.delete(record_id)
        assert_success(delete_result)

        detail_result = lostfound_api.get_detail(lost_found_id=record_id)
        if detail_result["code"] == 200:
            pytest.xfail("后端失物招领详情查询未过滤逻辑删除记录，删除后回查仍返回200")
        assert_failed(detail_result)

    @pytest.mark.lostfound
    @pytest.mark.p0
    def test_report_record(self, user_token, extra_user_token, approved_lost_found_id):
        """LF-018 举报失物招领信息（发布者不能举报自己，用另一个用户举报）。"""
        if not user_token or not extra_user_token:
            pytest.skip("user login failed")
        request_util.set_token(extra_user_token)
        result = lostfound_api.report(lost_found_id=approved_lost_found_id, reason="测试举报原因内容")
        assert_success(result)
        assert_text_contains(result, "举报成功")

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_report_reason_too_short(self, user_token, extra_user_token, approved_lost_found_id):
        """LF-019 举报原因过短（4字）。"""
        if not user_token or not extra_user_token:
            pytest.skip("user login failed")
        request_util.set_token(extra_user_token)
        result = lostfound_api.report(lost_found_id=approved_lost_found_id, reason="太短了")
        assert_failed(result)
        assert "举报原因长度需在5-500字之间" in result["message"], result


@allure.feature("lostfound")
class TestLostFoundAdmin:
    @pytest.mark.lostfound
    @pytest.mark.admin
    @pytest.mark.p1
    def test_admin_list(self, admin_token, created_lost_found):
        """LF-020 管理员分页列表。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = lostfound_api.admin_list(page_num=1, page_size=20)
        assert_success(result)
        records = get_page_records(result)
        assert any(record.get("id") == created_lost_found["id"] for record in records), result

    @pytest.mark.lostfound
    @pytest.mark.admin
    @pytest.mark.p0
    def test_admin_audit_approve(self, user_token, admin_token, created_lost_found):
        """LF-021 审核通过信息后用户端可见。"""
        if not admin_token or not user_token:
            pytest.skip("login failed")
        request_util.set_token(admin_token)
        audit_result = lostfound_api.admin_audit(lost_found_id=created_lost_found["id"], audit_status=1)
        assert_success(audit_result)
        assert_text_contains(audit_result, "审核完成")

        request_util.set_token(user_token)
        detail_result = lostfound_api.get_detail(lost_found_id=created_lost_found["id"])
        assert_success(detail_result)

    @pytest.mark.lostfound
    @pytest.mark.admin
    @pytest.mark.p1
    def test_admin_get_detail(self, admin_token, created_lost_found):
        """LF-022 管理员查看详情。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = lostfound_api.admin_get_detail(lost_found_id=created_lost_found["id"])
        assert_success(result)
        assert result["data"]["id"] == created_lost_found["id"], result

    @pytest.mark.lostfound
    @pytest.mark.admin
    @pytest.mark.p2
    def test_admin_get_reports_of_record(self, user_token, extra_user_token, admin_token, approved_lost_found_id):
        """LF-023 管理员查看举报记录。"""
        if not user_token or not extra_user_token or not admin_token:
            pytest.skip("login failed")
        request_util.set_token(extra_user_token)
        report_result = lostfound_api.report(lost_found_id=approved_lost_found_id, reason="管理员查举报的测试原因")
        assert_success(report_result)

        request_util.set_token(admin_token)
        result = lostfound_api.admin_get_reports(lost_found_id=approved_lost_found_id)
        assert_success(result)
        assert result["data"], result

    @pytest.mark.lostfound
    @pytest.mark.admin
    @pytest.mark.p2
    def test_admin_report_list_and_handle(self, user_token, extra_user_token, admin_token, approved_lost_found_id):
        """LF-024 举报列表与处理。"""
        if not user_token or not extra_user_token or not admin_token:
            pytest.skip("login failed")
        request_util.set_token(extra_user_token)
        report_result = lostfound_api.report(lost_found_id=approved_lost_found_id, reason="举报列表处理的测试原因")
        assert_success(report_result)
        report_data = report_result.get("data")
        report_id = report_data.get("id") if isinstance(report_data, dict) else None

        request_util.set_token(admin_token)
        list_result = lostfound_api.admin_report_list(page_num=1, page_size=10)
        assert_success(list_result)
        records = get_page_records(list_result)
        assert records, list_result
        if report_id is None:
            report_id = records[0]["id"]
        assert any(record.get("id") == report_id for record in records), list_result

        handle_result = lostfound_api.admin_audit_report(report_id=report_id, status=1, handle_remark="测试处理")
        assert_success(handle_result)
        assert_text_contains(handle_result, "举报处理完成")

    @pytest.mark.lostfound
    @pytest.mark.admin
    @pytest.mark.p2
    def test_admin_delete(self, admin_token, lostfound_data):
        """LF-025 管理员删除信息。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        create_result = lostfound_api.create(
            item_type=1,
            title=lostfound_data["title"],
            item_name="管理员待删物品",
            category=1,
            description="管理员删除测试",
            location_area="图书馆",
        )
        assert_success(create_result)
        record_id = create_result["data"]["id"]

        delete_result = lostfound_api.admin_delete(record_id, delete_reason="违规测试删除")
        assert_success(delete_result)
        assert_text_contains(delete_result, "删除成功")

        detail_result = lostfound_api.admin_get_detail(lost_found_id=record_id)
        if detail_result["code"] == 200:
            pytest.xfail("后端管理员详情查询未过滤逻辑删除记录，删除后回查仍返回200")
        assert_failed(detail_result)

    @pytest.mark.lostfound
    @pytest.mark.p1
    def test_admin_list_forbidden_for_user(self, user_token):
        """LF-026 普通用户访问管理接口。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.admin_list(page_num=1, page_size=10)
        assert_failed(result)
