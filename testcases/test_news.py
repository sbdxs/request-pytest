"""News API tests."""

from __future__ import annotations

import allure
import pytest

from api.news_api import news_api
from conftest import assert_failed, assert_success
from utils.request_util import request_util


@allure.feature("news")
class TestNewsList:
    @pytest.mark.news
    def test_list_news(self):
        result = news_api.list(page_num=1, page_size=10)
        assert_success(result)
        assert result["data"] is not None
        assert "records" in result["data"]

    @pytest.mark.news
    def test_get_slide_news(self):
        result = news_api.get_slide_news()
        assert_success(result)
        assert result["data"] is not None


@allure.feature("news")
class TestNewsDetail:
    @pytest.mark.news
    def test_get_news_detail(self, published_news_id):
        result = news_api.get_detail(news_id=published_news_id)
        assert_success(result)
        assert result["data"]["id"] == published_news_id
        assert result["data"]["title"]


@allure.feature("news")
class TestNewsAdmin:
    @pytest.mark.news
    @pytest.mark.admin
    def test_admin_get_all(self, admin_token):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = news_api.admin_get_all()
        assert_success(result)
        assert result["data"] is not None

    @pytest.mark.news
    @pytest.mark.admin
    def test_admin_create_news(self, admin_token, news_data):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = news_api.admin_create(
            title=news_data["title"],
            content=news_data["content"],
            author=news_data["author"],
            category=news_data["category"],
            status=news_data["status"],
            is_top=news_data["isTop"],
        )
        assert_success(result)
        data = result["data"]
        assert data["id"] is not None
        assert data["title"] == news_data["title"]

    @pytest.mark.news
    @pytest.mark.admin
    def test_admin_update_news(self, admin_token, news_data):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)

        create_result = news_api.admin_create(
            title=news_data["title"],
            content=news_data["content"],
            author=news_data["author"],
            category=news_data["category"],
            status=news_data["status"],
            is_top=news_data["isTop"],
        )
        assert_success(create_result)
        created = create_result["data"]

        updated_title = f'{news_data["title"]}-updated'
        updated_content = f'{news_data["content"]}\nupdated'
        update_result = news_api.admin_update(
            news_id=created["id"],
            title=updated_title,
            content=updated_content,
            author=news_data["author"],
            category=news_data["category"],
            status=news_data["status"],
            is_top=news_data["isTop"],
        )
        assert_success(update_result)
        updated = update_result["data"]
        assert updated["id"] == created["id"]
        assert updated["title"] == updated_title

        detail_result = news_api.get_detail(news_id=created["id"])
        assert_success(detail_result)
        assert detail_result["data"]["title"] == updated_title

    @pytest.mark.news
    @pytest.mark.admin
    def test_admin_delete_news(self, admin_token, news_data):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)

        create_result = news_api.admin_create(
            title=news_data["title"],
            content=news_data["content"],
            author=news_data["author"],
            category=news_data["category"],
            status=news_data["status"],
            is_top=news_data["isTop"],
        )
        assert_success(create_result)
        created_id = create_result["data"]["id"]

        delete_result = news_api.admin_delete(created_id)
        assert_success(delete_result)

        detail_result = news_api.get_detail(created_id)
        assert_failed(detail_result)

