"""User API tests."""

from __future__ import annotations

import allure
import pytest

from api.user_api import user_api
from conftest import assert_failed, assert_success, get_page_records
from testdata.user_cases import LOGIN_CASES, REGISTER_CASES
from utils.request_util import request_util
from utils.test_context import ADMIN_USERNAME


def _build_account(mode: str, created_login_user: dict) -> str:
    if mode == "admin_username":
        return ADMIN_USERNAME
    if mode == "not_exists":
        return "not_exist_user_for_test"
    if mode == "empty":
        return ""
    if mode == "fresh_username":
        return created_login_user["username"]
    if mode == "fresh_student_id":
        return created_login_user["studentId"]
    if mode == "fresh_phone":
        return created_login_user["phone"]
    raise ValueError(f"unknown account mode: {mode}")


def _build_login_password(mode: str, created_login_user: dict) -> str:
    if mode == "correct":
        return "123456"
    if mode == "wrong":
        return "wrong_password"
    if mode == "empty":
        return ""
    if mode == "fresh_user_password":
        return created_login_user["password"]
    raise ValueError(f"unknown login password mode: {mode}")


@allure.feature("user")
class TestUserRegister:
    @pytest.mark.user
    @pytest.mark.parametrize("case", REGISTER_CASES, ids=[case["id"] for case in REGISTER_CASES])
    def test_register_cases(self, case, register_data):
        username = case["username"] or register_data["username"]
        password = case["password"]
        email = case["email"] or register_data["email"]
        nickname = register_data["nickname"]
        student_id = register_data["studentId"]
        phone = register_data["phone"]

        if case["prepare_duplicate"]:
            first_result = user_api.register(
                username=username,
                password=register_data["password"],
                email=email,
                nickname=nickname,
                student_id=student_id,
                phone=phone,
            )
            assert_success(first_result)

        result = user_api.register(
            username=username,
            password=password,
            email=email,
            nickname=nickname,
            student_id=student_id,
            phone=phone,
        )

        if case["expected_success"]:
            assert_success(result)
            if case["expected_message_contains"]:
                assert case["expected_message_contains"] in result["message"], result
        else:
            assert_failed(result)
            if case["expected_message_contains"]:
                assert case["expected_message_contains"] in result["message"], result


@allure.feature("user")
class TestUserLogin:
    @pytest.mark.user
    @pytest.mark.parametrize("case", LOGIN_CASES, ids=[case["id"] for case in LOGIN_CASES])
    def test_login_cases(self, case, admin_token, created_login_user, current_user):
        banned_user_id = None
        if case["ban_user"]:
            if not admin_token:
                pytest.skip("admin login failed")
            request_util.set_token(admin_token)
            user_list_result = user_api.get_users(
                page_num=1,
                page_size=20,
                keyword=created_login_user["username"],
            )
            assert_success(user_list_result)
            records = get_page_records(user_list_result)
            target_user = next((user for user in records if user.get("username") == created_login_user["username"]), None)
            assert target_user is not None, user_list_result
            banned_user_id = target_user["id"]
            ban_result = user_api.ban_user(
                user_id=banned_user_id,
                ban_type=2,
                reason="test login ban case",
            )
            assert_success(ban_result)
            request_util.clear_headers()

        account = _build_account(case["account_mode"], created_login_user)
        password = _build_login_password(case["password_mode"], created_login_user)
        result = user_api.login(username=account, password=password)

        if case["expected_success"]:
            assert_success(result)
            assert result["data"] is not None, result
            assert result["data"].get("token"), result
            user_info = result["data"].get("user") or {}
            if case["account_mode"] == "admin_username":
                assert user_info.get("username") == ADMIN_USERNAME
            else:
                assert user_info.get("username") == created_login_user["username"]
        else:
            assert_failed(result)
            if "expected_code" in case:
                assert result["code"] == case["expected_code"], result
            if case.get("expected_message_contains"):
                assert case["expected_message_contains"] in result["message"], result

        if banned_user_id is not None:
            request_util.set_token(admin_token)
            unban_result = user_api.unban_user(banned_user_id)
            assert_success(unban_result)
            request_util.clear_headers()


@allure.feature("user")
class TestUserInfo:
    @pytest.mark.user
    def test_get_current_user(self, user_token, current_user):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = user_api.get_current_user()
        assert_success(result)
        data = result["data"]
        assert data["id"] == current_user["id"]
        assert data["username"] == current_user["username"]

    @pytest.mark.user
    def test_get_current_user_without_token(self):
        request_util.clear_headers()
        result = user_api.get_current_user()
        assert_failed(result)


@allure.feature("user")
class TestUserProfile:
    @pytest.mark.user
    def test_update_email(self, user_token):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        new_email = "test_profile_update@example.com"
        result = user_api.update_profile(email=new_email)
        assert_success(result)
        assert "成功" in result["message"]

        current_result = user_api.get_current_user()
        assert_success(current_result)
        assert current_result["data"]["email"] == new_email


@allure.feature("user")
class TestUserAdmin:
    @pytest.mark.user
    @pytest.mark.admin
    def test_get_dashboard(self, admin_token):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = user_api.get_dashboard()
        assert_success(result)
        assert result["data"] is not None

    @pytest.mark.user
    @pytest.mark.admin
    def test_get_users(self, admin_token, current_user):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = user_api.get_users(
            page_num=1,
            page_size=10,
            keyword=current_user["username"],
        )
        assert_success(result)
        records = get_page_records(result)
        assert records
        assert any(user.get("id") == current_user["id"] for user in records)
