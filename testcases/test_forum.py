"""Forum API tests."""

from __future__ import annotations

import allure
import pytest

from api.forum_api import forum_api
from conftest import assert_success, get_page_records
from utils.request_util import request_util


@allure.feature("forum")
class TestForumPost:
    @pytest.mark.forum
    def test_get_categories(self, user_token):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.get_categories()
        assert_success(result)
        categories = result["data"] or []
        assert categories
        assert categories[0]["id"] is not None

    @pytest.mark.forum
    def test_create_post(self, user_token, forum_post_data):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.create_post(
            title=forum_post_data["title"],
            content=forum_post_data["content"],
            category_id=forum_post_data["categoryId"],
        )
        assert_success(result)
        data = result["data"]
        assert data["id"] is not None
        assert data["title"] == forum_post_data["title"]
        assert data["content"] == forum_post_data["content"]

    @pytest.mark.forum
    def test_list_posts(self, user_token):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.list_posts(page_num=1, page_size=10)
        assert_success(result)
        assert result["data"] is not None
        assert "records" in result["data"]

    @pytest.mark.forum
    def test_get_post_detail(self, user_token, created_forum_post):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.get_post_detail(post_id=created_forum_post["id"])
        assert_success(result)
        data = result["data"]
        assert data["id"] == created_forum_post["id"]
        assert data["title"] == created_forum_post["title"]


@allure.feature("forum")
class TestForumComment:
    @pytest.mark.forum
    def test_list_comments(self, user_token, visible_forum_post_id):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.list_comments(post_id=visible_forum_post_id, page_num=1, page_size=10)
        assert_success(result)
        assert result["data"] is not None
        assert "records" in result["data"]


@allure.feature("forum")
class TestForumInteraction:
    @pytest.mark.forum
    def test_like_and_unlike(self, user_token, visible_forum_post_id):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)

        detail_before = forum_api.get_post_detail(post_id=visible_forum_post_id)
        assert_success(detail_before)
        like_count_before = detail_before["data"]["likeCount"]

        like_result = forum_api.like_post(post_id=visible_forum_post_id)
        assert_success(like_result)

        detail_after_like = forum_api.get_post_detail(post_id=visible_forum_post_id)
        assert_success(detail_after_like)
        assert detail_after_like["data"]["liked"] == 1
        assert detail_after_like["data"]["likeCount"] >= like_count_before + 1

        unlike_result = forum_api.unlike_post(post_id=visible_forum_post_id)
        assert_success(unlike_result)

        detail_after_unlike = forum_api.get_post_detail(post_id=visible_forum_post_id)
        assert_success(detail_after_unlike)
        assert detail_after_unlike["data"]["liked"] == 0


@allure.feature("forum")
class TestForumAdmin:
    @pytest.mark.forum
    @pytest.mark.admin
    def test_admin_list_pending(self, admin_token, created_forum_post):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        page_num = 1
        page_size = 20
        found = False

        while True:
            result = forum_api.admin_list_pending(page_num=page_num, page_size=page_size)
            assert_success(result)
            records = get_page_records(result)
            if any(post.get("id") == created_forum_post["id"] for post in records):
                found = True
                break

            data = result["data"] or {}
            total_pages = data.get("pages") or 1
            if page_num >= total_pages:
                break
            page_num += 1

        assert found, result
