"""论坛模块夹具：版块、发帖与审核前置数据。"""

from __future__ import annotations

import pytest

from api.forum_api import forum_api
from fixtures.helpers import FORUM_AUDIT_APPROVED, assert_success
from utils.data_util import data_util
from utils.request_util import request_util


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
