"""Parameterized cases aligned with current backend behavior."""

from __future__ import annotations


REGISTER_CASES = [
    {
        "id": "register_success_basic",
        "prepare_duplicate": False,
        "username": None,
        "password": "123456",
        "email": None,
        "expected_success": True,
        "expected_message_contains": "成功",
    },
    {
        "id": "register_duplicate_username",
        "prepare_duplicate": True,
        "username": None,
        "password": "123456",
        "email": None,
        "expected_success": False,
        "expected_message_contains": "存在",
    },
]


LOGIN_CASES = [
    {
        "id": "login_success_username",
        "account_mode": "admin_username",
        "password_mode": "correct",
        "ban_user": False,
        "expected_success": True,
        "expected_message_contains": None,
    },
    {
        "id": "login_wrong_password",
        "account_mode": "admin_username",
        "password_mode": "wrong",
        "ban_user": False,
        "expected_success": False,
        "expected_code": 400,
    },
    {
        "id": "login_user_not_found",
        "account_mode": "not_exists",
        "password_mode": "correct",
        "ban_user": False,
        "expected_success": False,
        "expected_code": 400,
    },
    {
        "id": "login_empty_account",
        "account_mode": "empty",
        "password_mode": "correct",
        "ban_user": False,
        "expected_success": False,
        "expected_code": 400,
    },
    {
        "id": "login_empty_password",
        "account_mode": "admin_username",
        "password_mode": "empty",
        "ban_user": False,
        "expected_success": False,
        "expected_code": 400,
    },
    {
        "id": "login_success_student_id",
        "account_mode": "fresh_student_id",
        "password_mode": "fresh_user_password",
        "ban_user": False,
        "expected_success": True,
        "expected_message_contains": None,
    },
    {
        "id": "login_success_phone",
        "account_mode": "fresh_phone",
        "password_mode": "fresh_user_password",
        "ban_user": False,
        "expected_success": True,
        "expected_message_contains": None,
    },
    {
        "id": "login_banned_user",
        "account_mode": "fresh_username",
        "password_mode": "fresh_user_password",
        "ban_user": True,
        "expected_success": False,
        "expected_code": 400,
        "expected_message_contains": "test login ban case",
    },
]
