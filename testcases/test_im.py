"""IM API tests — 对应 接口测试用例/05-私信模块用例.md (IM-001 ~ IM-013).

双账号约定：用户A = stu_zhang（user_token），用户B = 临时注册的 extra_user，用户C = admin（非会话参与者）。
"""

from __future__ import annotations

import allure
import pytest

from api.im_api import im_api
from conftest import assert_failed, assert_success, assert_text_contains, get_page_records
from utils.data_util import data_util
from utils.request_util import request_util


@pytest.fixture(scope="module")
def im_conversation_id(user_token, extra_user):
    """用户A与用户B之间创建的会话（module 级复用）。"""
    if not user_token:
        pytest.skip("user login failed")
    request_util.set_token(user_token)
    result = im_api.create_conversation(target_user_id=extra_user["id"])
    assert_success(result)
    conversation_id = (result["data"] or {}).get("id")
    if not conversation_id:
        pytest.skip("conversation create did not return id")
    return conversation_id


@pytest.fixture(scope="module")
def im_sent_message_id(user_token, im_conversation_id):
    """用户A发送的一条消息 id。"""
    request_util.set_token(user_token)
    result = im_api.send_message(
        conversation_id=im_conversation_id,
        content=f"测试消息内容_{data_util.generate_unique_id()}",
    )
    assert_success(result)
    message_id = (result["data"] or {}).get("id")
    if not message_id:
        pytest.skip("send message did not return id")
    return message_id


@allure.feature("im")
class TestImConversation:
    @pytest.mark.im
    @pytest.mark.p0
    def test_create_conversation(self, user_token, im_conversation_id):
        """IM-001 创建会话。"""
        assert im_conversation_id is not None

    @pytest.mark.im
    @pytest.mark.p1
    def test_create_conversation_repeat_same_id(self, user_token, extra_user, im_conversation_id):
        """IM-002 重复创建相同会话返回同一会话 id。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = im_api.create_conversation(target_user_id=extra_user["id"])
        assert_success(result)
        assert (result["data"] or {}).get("id") == im_conversation_id, result

    @pytest.mark.im
    @pytest.mark.p1
    def test_create_conversation_target_not_exist(self, user_token):
        """IM-003 目标用户不存在。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = im_api.create_conversation(target_user_id=999999)
        assert_failed(result)

    @pytest.mark.im
    @pytest.mark.p0
    def test_list_conversations_contains_target(self, user_token, extra_user, im_conversation_id):
        """IM-004 会话列表包含与用户B的会话。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = im_api.list_conversations()
        assert_success(result)
        data = result["data"] or {}
        if isinstance(data, dict):
            conversations = data.get("conversations") or data.get("records") or []
        else:
            conversations = data
        assert conversations, result
        assert any(
            conversation.get("id") == im_conversation_id
            for conversation in conversations
        ), result


@allure.feature("im")
class TestImMessage:
    @pytest.mark.im
    @pytest.mark.p0
    def test_send_message(self, im_sent_message_id):
        """IM-005 发送消息。"""
        assert im_sent_message_id is not None

    @pytest.mark.im
    @pytest.mark.p0
    def test_receiver_view_messages(self, extra_user, im_conversation_id, im_sent_message_id):
        """IM-006 接收方查看消息列表。"""
        request_util.set_token(extra_user["token"])
        result = im_api.list_messages(conversation_id=im_conversation_id, page_num=1, page_size=20)
        assert_success(result)
        records = get_page_records(result)
        assert any(message.get("id") == im_sent_message_id for message in records), result

    @pytest.mark.im
    @pytest.mark.p1
    def test_send_message_too_long(self, user_token, im_conversation_id):
        """IM-007 消息超长（1001字）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = im_api.send_message(conversation_id=im_conversation_id, content="长" * 1001)
        assert_failed(result)
        assert "消息长度必须在1到1000之间" in result["message"], result

    @pytest.mark.im
    @pytest.mark.p1
    def test_send_message_empty(self, user_token, im_conversation_id):
        """IM-008 空内容消息（@NotBlank 与 @Size 校验提示顺序不固定，两者皆可）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = im_api.send_message(conversation_id=im_conversation_id, content="")
        assert_failed(result)
        assert (
            "消息内容不能为空" in result["message"] or "消息长度必须在1到1000之间" in result["message"]
        ), result

    @pytest.mark.im
    @pytest.mark.p1
    def test_non_participant_cannot_view_messages(self, admin_token, im_conversation_id):
        """IM-009 非会话参与者查看消息。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = im_api.list_messages(conversation_id=im_conversation_id, page_num=1, page_size=20)
        assert_failed(result)


@allure.feature("im")
class TestImReadAndUnread:
    @pytest.mark.im
    @pytest.mark.p1
    def test_mark_read(self, extra_user, im_conversation_id):
        """IM-010 标记会话已读。"""
        request_util.set_token(extra_user["token"])
        result = im_api.mark_read(conversation_id=im_conversation_id)
        assert_success(result)
        assert_text_contains(result, "已标记为已读")

    @pytest.mark.im
    @pytest.mark.p1
    def test_unread_count(self, extra_user):
        """IM-011 未读消息计数为非负数字。"""
        request_util.set_token(extra_user["token"])
        result = im_api.get_unread_count()
        assert_success(result)
        assert isinstance(result["data"], int) and result["data"] >= 0, result


@allure.feature("im")
class TestImReport:
    @pytest.mark.im
    @pytest.mark.p1
    def test_report_message_and_admin_handle(self, extra_user, admin_token, im_sent_message_id):
        """IM-012 举报消息并处理。"""
        request_util.set_token(extra_user["token"])
        report_result = im_api.report_message(message_id=im_sent_message_id, reason="测试举报消息")
        assert_success(report_result)
        report_data = report_result.get("data")
        report_id = report_data.get("id") if isinstance(report_data, dict) else None

        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        list_result = im_api.admin_list_reports(page_num=1, page_size=10)
        assert_success(list_result)
        records = get_page_records(list_result)
        assert records, list_result
        if report_id is None:
            report_id = records[0]["id"]
        assert any(report.get("id") == report_id for report in records), list_result

        handle_result = im_api.admin_audit_report(report_id=report_id, status=1)
        assert_success(handle_result)
        assert_text_contains(handle_result, "审核完成")


@allure.feature("im")
class TestImPermission:
    @pytest.mark.im
    @pytest.mark.p2
    def test_list_conversations_without_token(self):
        """IM-013 未登录访问私信接口。"""
        request_util.clear_headers()
        result = im_api.list_conversations()
        assert_failed(result)
        assert result["code"] == 401, result
