"""News API tests — 对应 接口测试用例/04-新闻公告模块用例.md (NEWS-001 ~ NEWS-013)."""

from __future__ import annotations

import allure
import pytest

from api.news_api import news_api
from conftest import assert_failed, assert_success, assert_text_contains, get_page_records
from utils.request_util import request_util


@allure.feature("news")
class TestNewsBrowse:
    @pytest.mark.news
    @pytest.mark.p0
    def test_list_news(self):
        """NEWS-001 已发布新闻列表（无需登录）。"""
        request_util.clear_headers()
        result = news_api.list(page_num=1, page_size=10)
        assert_success(result)
        records = get_page_records(result)
        assert records, result

    @pytest.mark.news
    @pytest.mark.p1
    def test_list_news_filter_by_category(self):
        """NEWS-002 按分类筛选。"""
        request_util.clear_headers()
        result = news_api.list(page_num=1, page_size=10, category=1)
        assert_success(result)
        for record in get_page_records(result):
            assert record.get("category") == 1, record

    @pytest.mark.news
    @pytest.mark.p1
    def test_list_news_page_size(self):
        """NEWS-003 分页参数生效。"""
        request_util.clear_headers()
        result = news_api.list(page_num=1, page_size=1)
        assert_success(result)
        records = get_page_records(result)
        assert len(records) <= 1, result

    @pytest.mark.news
    @pytest.mark.p0
    def test_get_news_detail(self, published_news_id):
        """NEWS-004 查看新闻详情。"""
        request_util.clear_headers()
        result = news_api.get_detail(news_id=published_news_id)
        assert_success(result)
        data = result["data"]
        assert data["id"] == published_news_id, result
        assert data.get("title"), result
        assert data.get("content"), result

    @pytest.mark.news
    @pytest.mark.p1
    def test_get_news_detail_not_exist(self):
        """NEWS-005 查看不存在的新闻。"""
        request_util.clear_headers()
        result = news_api.get_detail(news_id=999999)
        assert_failed(result)
        assert "新闻不存在" in result["message"], result

    @pytest.mark.news
    @pytest.mark.p1
    def test_get_slide_news(self):
        """NEWS-006 获取轮播新闻。"""
        request_util.clear_headers()
        result = news_api.get_slide_news()
        assert_success(result)
        assert isinstance(result["data"], list), result


@allure.feature("news")
class TestNewsAdmin:
    @pytest.mark.news
    @pytest.mark.admin
    @pytest.mark.p0
    def test_admin_create_news(self, admin_token, news_data):
        """NEWS-007 创建新闻。"""
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
        assert data["id"] is not None, result

    @pytest.mark.news
    @pytest.mark.admin
    @pytest.mark.p0
    def test_admin_create_then_visible_in_user_list(self, admin_token, news_data):
        """NEWS-008 创建后在用户端列表可见。"""
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

        request_util.clear_headers()
        list_result = news_api.list(page_num=1, page_size=10)
        assert_success(list_result)
        records = get_page_records(list_result)
        assert any(news.get("id") == created_id for news in records), list_result

    @pytest.mark.news
    @pytest.mark.admin
    @pytest.mark.p0
    def test_admin_update_news(self, admin_token, news_data):
        """NEWS-009 更新新闻后回查生效。"""
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
        update_result = news_api.admin_update(
            news_id=created["id"],
            title=updated_title,
            content=news_data["content"],
            author=news_data["author"],
            category=news_data["category"],
            status=news_data["status"],
            is_top=news_data["isTop"],
        )
        assert_success(update_result)

        detail_result = news_api.get_detail(news_id=created["id"])
        assert_success(detail_result)
        assert detail_result["data"]["title"] == updated_title, detail_result

    @pytest.mark.news
    @pytest.mark.admin
    @pytest.mark.p0
    def test_admin_delete_news(self, admin_token, news_data):
        """NEWS-010 删除新闻后回查不存在。"""
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
        assert_text_contains(delete_result, "删除成功")

        detail_result = news_api.get_detail(created_id)
        assert_failed(detail_result)
        assert "新闻不存在" in detail_result["message"], detail_result

    @pytest.mark.news
    @pytest.mark.admin
    @pytest.mark.p1
    def test_admin_get_all(self, admin_token):
        """NEWS-011 管理员查询全部新闻（含未发布）。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        admin_result = news_api.admin_get_all()
        assert_success(admin_result)
        assert admin_result["data"] is not None

        request_util.clear_headers()
        user_result = news_api.list(page_num=1, page_size=50)
        assert_success(user_result)
        user_records = get_page_records(user_result)
        assert all(news.get("status") == 1 for news in user_records), user_result

    @pytest.mark.news
    @pytest.mark.admin
    @pytest.mark.p2
    def test_admin_get_page(self, admin_token):
        """NEWS-012 管理员分页查询。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = news_api.admin_get_page(page_num=1, page_size=5)
        assert_success(result)
        assert "records" in (result["data"] or {}), result
        assert "total" in (result["data"] or {}), result

    @pytest.mark.news
    @pytest.mark.p1
    def test_admin_create_forbidden(self, user_token):
        """NEWS-013 越权与未登录访问管理接口。"""
        news_payload = {"title": "越权测试", "content": "越权测试内容", "author": "user", "category": 1, "status": 1}

        if user_token:
            request_util.set_token(user_token)
            user_result = news_api.admin_create(
                title=news_payload["title"],
                content=news_payload["content"],
                author=news_payload["author"],
                category=news_payload["category"],
                status=news_payload["status"],
            )
            assert_failed(user_result)

        request_util.clear_headers()
        anonymous_result = news_api.admin_create(
            title=news_payload["title"],
            content=news_payload["content"],
            author=news_payload["author"],
            category=news_payload["category"],
            status=news_payload["status"],
        )
        assert_failed(anonymous_result)
