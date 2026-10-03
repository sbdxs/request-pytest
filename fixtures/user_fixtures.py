"""用户模块夹具：注册/登录数据、动态用户与上传文件。"""

from __future__ import annotations

import pytest

from api.user_api import user_api
from fixtures.helpers import (
    assert_success,
    build_unique_phone,
    build_unique_student_id,
    get_page_records,
)
from utils.data_util import data_util
from utils.request_util import request_util
from utils.test_context import ADMIN_USERNAME, TARGET_USER_ID


@pytest.fixture
def register_data():
    unique_seed = data_util.generate_unique_id()
    return {
        "username": data_util.generate_username(),
        "password": "123456",
        "email": data_util.generate_email(),
        "nickname": data_util.generate_nickname(),
        "studentId": build_unique_student_id(unique_seed),
        "phone": build_unique_phone(unique_seed),
    }


@pytest.fixture
def login_data():
    return {"username": ADMIN_USERNAME, "password": "123456"}


@pytest.fixture(scope="session")
def current_user(user_token):
    if not user_token:
        pytest.skip("user login failed")
    request_util.set_token(user_token)
    result = user_api.get_current_user()
    request_util.clear_headers()
    assert_success(result)
    return result["data"]


@pytest.fixture(scope="session")
def target_user_id(current_user, admin_token):
    current_user_id = current_user["id"]
    if TARGET_USER_ID and TARGET_USER_ID != current_user_id:
        return TARGET_USER_ID
    if not admin_token:
        pytest.skip("admin login failed")
    request_util.set_token(admin_token)
    result = user_api.get_users(page_num=1, page_size=20)
    request_util.clear_headers()
    assert_success(result)
    records = get_page_records(result)
    for user in records:
        if user.get("id") != current_user_id:
            return user["id"]
    pytest.skip("no secondary user available for IM tests")


@pytest.fixture(scope="session")
def extra_user():
    """注册并登录一个临时普通用户，用于非作者/接收方/非参与者等双账号场景。"""
    unique_seed = data_util.generate_unique_id()
    suffix = unique_seed.replace("_", "")[:12]
    username = f"extra_{suffix}"
    password = "123456"
    email = f"extra_{suffix}@example.com"
    register_result = user_api.register(
        username=username,
        password=password,
        email=email,
        nickname=data_util.generate_nickname(),
        student_id=build_unique_student_id(unique_seed),
        phone=build_unique_phone(unique_seed),
    )
    assert_success(register_result)

    login_result = user_api.login(username=username, password=password)
    assert_success(login_result)
    login_data = login_result["data"] or {}
    user_info = login_data.get("user") or {}
    return {
        "id": user_info.get("id"),
        "username": username,
        "password": password,
        "token": login_data.get("token"),
    }


@pytest.fixture(scope="session")
def extra_user_token(extra_user):
    return extra_user["token"]


@pytest.fixture(scope="session")
def upload_file_factory(tmp_path_factory):
    """生成上传用临时文件（默认 1x1 PNG）。"""
    upload_dir = tmp_path_factory.mktemp("upload_files")

    def _create(filename: str, content: bytes | None = None) -> str:
        path = upload_dir / filename
        path.write_bytes(content if content is not None else data_util.PNG_BYTES)
        return str(path)

    return _create


@pytest.fixture
def login_user_data():
    unique_seed = data_util.generate_unique_id()
    unique_suffix = unique_seed.replace("_", "")
    return {
        "username": f"login_{unique_suffix[:12]}",
        "password": "123456",
        "email": f"login_{unique_suffix[:12]}@example.com",
        "nickname": data_util.generate_nickname(),
        "studentId": build_unique_student_id(unique_seed),
        "phone": build_unique_phone(unique_seed),
    }


@pytest.fixture
def created_login_user(login_user_data):
    result = user_api.register(
        username=login_user_data["username"],
        password=login_user_data["password"],
        email=login_user_data["email"],
        nickname=login_user_data["nickname"],
        student_id=login_user_data["studentId"],
        phone=login_user_data["phone"],
    )
    assert_success(result)
    return login_user_data
