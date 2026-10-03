"""pytest fixtures and hooks.

本文件只保留：全局断言助手（再导出）、会话级登录态、autouse 环境夹具与报告 hook；
各业务模块夹具拆分在 fixtures/ 包内，通过 pytest_plugins 注册。
"""

from __future__ import annotations

import json
import socket
from urllib.parse import urlparse

import allure
import pytest
from loguru import logger

from fixtures.helpers import (  # noqa: F401 -- 再导出，保持 `from conftest import ...` 的既有用法
    assert_failed,
    assert_success,
    assert_text_contains,
    get_page_records,
    result_text,
)
from utils.auth_util import auth_util
from utils.request_util import request_util

pytest_plugins = [
    "fixtures.user_fixtures",
    "fixtures.forum_fixtures",
    "fixtures.lostfound_fixtures",
    "fixtures.news_fixtures",
    "fixtures.im_fixtures",
]


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


@pytest.fixture
def report_data():
    return {"reason": "test report reason long enough"}


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
