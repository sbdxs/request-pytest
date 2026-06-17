"""IM API tests."""

from __future__ import annotations

import allure
import pytest

from api.im_api import im_api
from conftest import assert_success
from utils.request_util import request_util


@allure.feature("im")
class TestImConversation:
    @pytest.mark.im
    def test_create_conversation(self, user_token, target_user_id):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = im_api.create_conversation(target_user_id=target_user_id)
        assert_success(result)
        data = result["data"]
        assert data["id"] is not None

    @pytest.mark.im
    def test_list_conversations(self, user_token):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = im_api.list_conversations()
        assert_success(result)
        assert result["data"] is not None


@allure.feature("im")
class TestImMessage:
    @pytest.mark.im
    def test_send_text_message(self, user_token, im_message_data, target_user_id):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        conversation = im_api.create_conversation(target_user_id=target_user_id)
        if not conversation["success"] or not conversation["data"]:
            pytest.skip("conversation create failed")
        result = im_api.send_message(
            conversation_id=conversation["data"]["id"],
            content=im_message_data["content"],
        )
        assert_success(result)
        data = result["data"]
        assert data["id"] is not None


@allure.feature("im")
class TestImAdmin:
    @pytest.mark.im
    @pytest.mark.admin
    def test_admin_list_reports(self, admin_token):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = im_api.admin_list_reports(page_num=1, page_size=10)
        assert_success(result)
        assert result["data"] is not None
