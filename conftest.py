"""pytest fixtures and hooks."""

from __future__ import annotations

import json
import socket
from urllib.parse import urlparse

import allure
import pytest
from loguru import logger

from api.forum_api import forum_api
from api.lostfound_api import lostfound_api
from api.news_api import news_api
from api.user_api import user_api
from utils.auth_util import auth_util
from utils.data_util import data_util
from utils.request_util import request_util
from utils.test_context import ADMIN_USERNAME, TARGET_USER_ID


FORUM_AUDIT_APPROVED = 1
LOST_FOUND_AUDIT_APPROVED = 1


def assert_success(result: dict, *, status_code: int = 200) -> None:
    assert result["status_code"] == status_code, result
    assert result["success"] is True, result
    assert result["code"] == 200, result


def assert_failed(result: dict, *, status_code: int | None = None) -> None:
    assert result["success"] is False, result
    if status_code is not None:
        assert result["status_code"] == status_code, result
    assert result["code"] != 200, result


def get_page_records(result: dict) -> list[dict]:
    data = result.get("data") or {}
    return data.get("records") or []


def _digits_only(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    return digits or "0"


def _build_unique_student_id(seed: str) -> str:
    digits = _digits_only(seed)
    return digits[-10:].rjust(10, "0")


def _build_unique_phone(seed: str) -> str:
    digits = _digits_only(seed)
    return f"13{digits[-9:].rjust(9, '0')}"


def attach_last_exchange() -> None:
    allure.attach(
        request_util.dump_last_exchange(),
        name="http_exchange",
        attachment_type=allure.attachment_type.JSON,
    )


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    parsed = urlparse(request_util.base_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        with socket.create_connection((host, port), timeout=3):
            pass
    except OSError as exc:
        pytest.skip(f"backend service unavailable at {request_util.base_url}: {exc}")

    logger.info("test session started")
    yield
    logger.info("test session finished")
    request_util.clear_headers()


@pytest.fixture(scope="function", autouse=True)
def setup_function():
    request_util.clear_headers()
    yield
    request_util.clear_headers()


@pytest.fixture(scope="session")
def admin_token():
    result = auth_util.admin_login()
    token = auth_util.get_token() if result else None
    yield token
    auth_util.logout()


@pytest.fixture(scope="session")
def user_token():
    result = auth_util.user_login()
    token = auth_util.get_token() if result else None
    yield token
    auth_util.logout()


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


@pytest.fixture
def register_data():
    unique_seed = data_util.generate_unique_id()
    return {
        "username": data_util.generate_username(),
        "password": "123456",
        "email": data_util.generate_email(),
        "nickname": data_util.generate_nickname(),
        "studentId": _build_unique_student_id(unique_seed),
        "phone": _build_unique_phone(unique_seed),
    }


@pytest.fixture
def login_data():
    return {"username": ADMIN_USERNAME, "password": "123456"}


@pytest.fixture
def login_user_data():
    unique_seed = data_util.generate_unique_id()
    unique_suffix = unique_seed.replace("_", "")
    return {
        "username": f"login_{unique_suffix[:12]}",
        "password": "123456",
        "email": f"login_{unique_suffix[:12]}@example.com",
        "nickname": data_util.generate_nickname(),
        "studentId": _build_unique_student_id(unique_seed),
        "phone": _build_unique_phone(unique_seed),
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


@pytest.fixture
def lostfound_data():
    return {
        "type": 1,
        "title": data_util.generate_title("lost"),
        "description": data_util.generate_content(),
        "itemName": "wallet",
        "category": 1,
        "locationArea": "图书馆",
        "locationDetail": "二楼自习区",
        "contactWay": 3,
        "isContactPublic": 0,
    }


@pytest.fixture(scope="session")
def forum_category_id(user_token):
    if not user_token:
        pytest.skip("user login failed")
    request_util.set_token(user_token)
    result = forum_api.get_categories()
    request_util.clear_headers()
    assert_success(result)
    categories = result.get("data") or []
    if not categories:
        pytest.skip("no forum category available")
    return categories[0]["id"]


@pytest.fixture
def forum_post_data(forum_category_id):
    return {
        "categoryId": forum_category_id,
        "title": data_util.generate_title("post"),
        "content": data_util.generate_content(),
    }


@pytest.fixture
def forum_comment_data():
    return {"content": data_util.generate_content(paragraphs=1)}


@pytest.fixture
def news_data():
    return {
        "title": data_util.generate_title("news"),
        "content": data_util.generate_content(),
        "author": "admin",
        "category": 1,
        "status": 1,
        "isTop": 0,
    }


@pytest.fixture
def im_message_data():
    return {"content": data_util.generate_content(paragraphs=1)}


@pytest.fixture
def report_data():
    return {"reason": "test report reason long enough"}


@pytest.fixture(scope="session")
def published_news_id():
    result = news_api.list(page_num=1, page_size=5)
    assert_success(result)
    records = get_page_records(result)
    if not records:
        pytest.skip("no published news available")
    return records[0]["id"]


@pytest.fixture
def created_forum_post(user_token, forum_post_data):
    if not user_token:
        pytest.skip("user login failed")
    request_util.set_token(user_token)
    result = forum_api.create_post(
        title=forum_post_data["title"],
        content=forum_post_data["content"],
        category_id=forum_post_data["categoryId"],
    )
    assert_success(result)
    data = result["data"] or {}
    post_id = data.get("id")
    if not post_id:
        pytest.skip("forum post create did not return post id")
    return data


@pytest.fixture
def approved_forum_post_id(admin_token, created_forum_post):
    if not admin_token:
        pytest.skip("admin login failed")
    request_util.set_token(admin_token)
    audit_result = forum_api.admin_audit_post(
        post_id=created_forum_post["id"],
        audit_status=FORUM_AUDIT_APPROVED,
    )
    assert_success(audit_result)
    return created_forum_post["id"]


@pytest.fixture
def visible_forum_post_id(user_token, approved_forum_post_id):
    if not user_token:
        pytest.skip("user login failed")
    request_util.set_token(user_token)
    detail_result = forum_api.get_post_detail(post_id=approved_forum_post_id)
    if not detail_result["success"]:
        pytest.skip("approved forum post is not accessible")
    return approved_forum_post_id


@pytest.fixture
def created_lost_found(user_token, lostfound_data):
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
    data = result["data"] or {}
    record_id = data.get("id")
    if not record_id:
        pytest.skip("lost found create did not return record id")
    return data


@pytest.fixture
def approved_lost_found_id(admin_token, created_lost_found):
    if not admin_token:
        pytest.skip("admin login failed")
    request_util.set_token(admin_token)
    audit_result = lostfound_api.admin_audit(
        lost_found_id=created_lost_found["id"],
        audit_status=LOST_FOUND_AUDIT_APPROVED,
    )
    assert_success(audit_result)
    return created_lost_found["id"]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if call.when != "call":
        return

    allure.attach(
        json.dumps(
            {
                "test_name": item.name,
                "status": report.outcome,
                "duration": call.duration,
            },
            ensure_ascii=False,
            indent=2,
        ),
        name="test_meta",
        attachment_type=allure.attachment_type.JSON,
    )
    attach_last_exchange()
    if report.failed:
        allure.attach(str(call.excinfo), name="failure", attachment_type=allure.attachment_type.TEXT)
