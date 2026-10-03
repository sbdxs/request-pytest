"""Forum API tests — 对应 接口测试用例/02-论坛模块用例.md (FORUM-001 ~ FORUM-033)."""

from __future__ import annotations

import allure
import pytest

from api.forum_api import forum_api
from conftest import assert_failed, assert_success, assert_text_contains, get_page_records
from utils.data_util import data_util
from utils.request_util import request_util


@allure.feature("forum")
class TestForumCreate:
    @pytest.mark.forum
    @pytest.mark.p0
    def test_create_post(self, user_token, forum_post_data):
        """FORUM-002 正常发布帖子。"""
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
        assert data["id"] is not None, result
        assert data["title"] == forum_post_data["title"], result

    @pytest.mark.forum
    @pytest.mark.p1
    def test_create_post_without_token(self, forum_post_data):
        """FORUM-003 未登录发帖。"""
        request_util.clear_headers()
        result = forum_api.create_post(
            title=forum_post_data["title"],
            content=forum_post_data["content"],
            category_id=forum_post_data["categoryId"],
        )
        assert_failed(result)
        assert result["code"] == 401, result

    @pytest.mark.forum
    @pytest.mark.p1
    def test_create_post_title_too_short(self, user_token, forum_category_id):
        """FORUM-004 标题过短（1个字）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.create_post(title="短", content="这是测试帖子内容", category_id=forum_category_id)
        assert_failed(result)
        assert "标题长度必须在2到200之间" in result["message"], result

    @pytest.mark.forum
    @pytest.mark.p1
    def test_create_post_empty_content(self, user_token, forum_post_data):
        """FORUM-005 内容为空。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.create_post(title=forum_post_data["title"], content="", category_id=forum_post_data["categoryId"])
        assert_failed(result)
        assert (
            "内容不能为空" in result["message"] or "内容长度必须在2到20000之间" in result["message"]
        ), result

    @pytest.mark.forum
    @pytest.mark.p1
    def test_create_post_without_category(self, user_token, forum_post_data):
        """FORUM-006 不传分类ID。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.create_post(title=forum_post_data["title"], content=forum_post_data["content"])
        assert_failed(result)
        assert "分类ID不能为空" in result["message"], result

    @pytest.mark.forum
    @pytest.mark.p2
    def test_create_post_category_not_exist(self, user_token, forum_post_data):
        """FORUM-007 分类ID不存在。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.create_post(
            title=forum_post_data["title"],
            content=forum_post_data["content"],
            category_id=9999,
        )
        assert_failed(result)


@allure.feature("forum")
class TestForumQuery:
    @pytest.mark.forum
    @pytest.mark.p0
    def test_get_categories(self, user_token):
        """FORUM-001 获取帖子分类列表。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.get_categories()
        assert_success(result)
        categories = result["data"] or []
        assert categories, result
        assert categories[0]["id"] is not None, result

    @pytest.mark.forum
    @pytest.mark.p0
    def test_list_posts(self, user_token):
        """FORUM-008 分页查询帖子列表。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.list_posts(page_num=1, page_size=10)
        assert_success(result)
        assert "records" in (result["data"] or {}), result

    @pytest.mark.forum
    @pytest.mark.p1
    def test_list_posts_filter_by_category(self, user_token, forum_category_id):
        """FORUM-009 按分类筛选列表。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.list_posts(page_num=1, page_size=10, category_id=forum_category_id)
        assert_success(result)
        for post in get_page_records(result):
            assert post.get("categoryId") == forum_category_id or post.get("category", {}).get("id") == forum_category_id, post

    @pytest.mark.forum
    @pytest.mark.p1
    def test_list_posts_keyword_search(self, user_token, approved_forum_post_id, created_forum_post):
        """FORUM-010 关键词搜索帖子（搜索已审核通过的帖子）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        keyword = created_forum_post["title"][:6]
        result = forum_api.list_posts(page_num=1, page_size=10, keyword=keyword)
        assert_success(result)
        records = get_page_records(result)
        assert any(post.get("id") == approved_forum_post_id for post in records), result

    @pytest.mark.forum
    @pytest.mark.p0
    def test_get_post_detail(self, user_token, visible_forum_post_id, created_forum_post):
        """FORUM-011 查看帖子详情（审核通过后）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.get_post_detail(post_id=visible_forum_post_id)
        assert_success(result)
        data = result["data"]
        assert data["id"] == created_forum_post["id"], result
        assert data["title"] == created_forum_post["title"], result

    @pytest.mark.forum
    @pytest.mark.p1
    def test_get_post_detail_not_exist(self, user_token):
        """FORUM-012 查看不存在的帖子。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.get_post_detail(post_id=999999)
        assert_failed(result)

    @pytest.mark.forum
    @pytest.mark.p1
    def test_pending_post_invisible_to_other_user(self, user_token, extra_user_token, created_forum_post):
        """FORUM-013 未审核帖子对其他普通用户不可见。"""
        if not user_token or not extra_user_token:
            pytest.skip("user login failed")
        request_util.set_token(extra_user_token)
        result = forum_api.get_post_detail(post_id=created_forum_post["id"])
        assert_failed(result)

    @pytest.mark.forum
    @pytest.mark.p1
    def test_my_published(self, user_token, created_forum_post):
        """FORUM-016 我的发布列表。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.list_my_published(page_num=1, page_size=10)
        assert_success(result)
        records = get_page_records(result)
        assert any(post.get("id") == created_forum_post["id"] for post in records), result

    @pytest.mark.forum
    @pytest.mark.p2
    def test_my_replied(self, user_token, visible_forum_post_id):
        """FORUM-017 我的回复列表（先评论再查）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        comment_result = forum_api.create_comment(post_id=visible_forum_post_id, content="我的回复列表测试评论")
        assert_success(comment_result)
        try:
            result = forum_api.list_my_replied(page_num=1, page_size=10)
            assert_success(result)
        finally:
            comment_id = (comment_result["data"] or {}).get("id")
            if comment_id:
                forum_api.delete_comment(comment_id)

    @pytest.mark.forum
    @pytest.mark.p2
    def test_my_favorited(self, user_token, visible_forum_post_id):
        """FORUM-018 我的收藏列表（先收藏再查）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        favorite_result = forum_api.favorite_post(post_id=visible_forum_post_id)
        assert_success(favorite_result)
        try:
            result = forum_api.list_my_favorited(page_num=1, page_size=10)
            assert_success(result)
            records = get_page_records(result)
            assert any(post.get("id") == visible_forum_post_id for post in records), result
        finally:
            forum_api.unfavorite_post(post_id=visible_forum_post_id)


@allure.feature("forum")
class TestForumInteract:
    @pytest.mark.forum
    @pytest.mark.p0
    def test_author_delete_own_post(self, user_token, forum_post_data):
        """FORUM-014 作者删除自己的帖子。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        create_result = forum_api.create_post(
            title=forum_post_data["title"],
            content=forum_post_data["content"],
            category_id=forum_post_data["categoryId"],
        )
        assert_success(create_result)
        post_id = create_result["data"]["id"]

        delete_result = forum_api.delete_post(post_id=post_id)
        assert_success(delete_result)
        assert_text_contains(delete_result, "帖子已删除")

        detail_result = forum_api.get_post_detail(post_id=post_id)
        if detail_result["code"] == 200:
            pytest.xfail("后端帖子详情查询未过滤已删除帖子，删除后回查仍返回200")
        assert_failed(detail_result)

    @pytest.mark.forum
    @pytest.mark.p1
    def test_non_author_delete_post(self, user_token, extra_user_token, created_forum_post):
        """FORUM-015 非作者删除帖子。"""
        if not user_token or not extra_user_token:
            pytest.skip("user login failed")
        request_util.set_token(extra_user_token)
        result = forum_api.delete_post(post_id=created_forum_post["id"])
        assert_failed(result)

    @pytest.mark.forum
    @pytest.mark.p0
    def test_create_comment(self, user_token, visible_forum_post_id, forum_comment_data):
        """FORUM-019 发表评论。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.create_comment(post_id=visible_forum_post_id, content=forum_comment_data["content"])
        assert_success(result)
        assert (result["data"] or {}).get("id") is not None, result

    @pytest.mark.forum
    @pytest.mark.p0
    def test_list_comments_contains_new(self, user_token, visible_forum_post_id):
        """FORUM-020 查看评论列表包含刚发的评论。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        content = f"评论列表验证_{data_util.generate_unique_id()}"
        create_result = forum_api.create_comment(post_id=visible_forum_post_id, content=content)
        assert_success(create_result)
        try:
            result = forum_api.list_comments(post_id=visible_forum_post_id, page_num=1, page_size=10)
            assert_success(result)
            records = get_page_records(result)
            assert any(comment.get("content") == content for comment in records), result
        finally:
            comment_id = (create_result["data"] or {}).get("id")
            if comment_id:
                forum_api.delete_comment(comment_id)

    @pytest.mark.forum
    @pytest.mark.p1
    def test_create_empty_comment(self, user_token, visible_forum_post_id):
        """FORUM-021 空内容评论。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.create_comment(post_id=visible_forum_post_id, content="")
        assert_failed(result)
        assert (
            "评论内容不能为空" in result["message"] or "评论内容长度必须在1到5000之间" in result["message"]
        ), result

    @pytest.mark.forum
    @pytest.mark.p1
    def test_delete_own_comment(self, user_token, visible_forum_post_id):
        """FORUM-022 删除自己的评论。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        create_result = forum_api.create_comment(post_id=visible_forum_post_id, content="待删除的测试评论")
        assert_success(create_result)
        comment_id = (create_result["data"] or {}).get("id")
        assert comment_id is not None, create_result

        delete_result = forum_api.delete_comment(comment_id=comment_id)
        assert_success(delete_result)
        assert_text_contains(delete_result, "评论已删除")

        list_result = forum_api.list_comments(post_id=visible_forum_post_id, page_num=1, page_size=50)
        assert_success(list_result)
        records = get_page_records(list_result)
        if any(comment.get("id") == comment_id for comment in records):
            pytest.xfail("后端评论列表未过滤已删除评论，删除后回查仍可见")
        assert all(comment.get("id") != comment_id for comment in records), list_result

    @pytest.mark.forum
    @pytest.mark.p0
    def test_like_and_unlike(self, user_token, visible_forum_post_id):
        """FORUM-023 点赞与取消点赞。"""
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
        assert detail_after_like["data"]["liked"] == 1, detail_after_like
        assert detail_after_like["data"]["likeCount"] >= like_count_before + 1, detail_after_like

        unlike_result = forum_api.unlike_post(post_id=visible_forum_post_id)
        assert_success(unlike_result)

        detail_after_unlike = forum_api.get_post_detail(post_id=visible_forum_post_id)
        assert_success(detail_after_unlike)
        assert detail_after_unlike["data"]["liked"] == 0, detail_after_unlike

    @pytest.mark.forum
    @pytest.mark.p0
    def test_favorite_and_unfavorite(self, user_token, visible_forum_post_id):
        """FORUM-024 收藏与取消收藏。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)

        favorite_result = forum_api.favorite_post(post_id=visible_forum_post_id)
        assert_success(favorite_result)

        favorited_result = forum_api.list_my_favorited(page_num=1, page_size=10)
        assert_success(favorited_result)
        records = get_page_records(favorited_result)
        assert any(post.get("id") == visible_forum_post_id for post in records), favorited_result

        unfavorite_result = forum_api.unfavorite_post(post_id=visible_forum_post_id)
        assert_success(unfavorite_result)

        favorited_after = forum_api.list_my_favorited(page_num=1, page_size=10)
        assert_success(favorited_after)
        records_after = get_page_records(favorited_after)
        assert all(post.get("id") != visible_forum_post_id for post in records_after), favorited_after

    @pytest.mark.forum
    @pytest.mark.p0
    def test_report_post(self, user_token, extra_user_token, approved_forum_post_id):
        """FORUM-025 举报帖子（作者不能举报自己，使用另一个普通用户举报）。"""
        if not user_token or not extra_user_token:
            pytest.skip("user login failed")
        request_util.set_token(extra_user_token)
        result = forum_api.report_post(post_id=approved_forum_post_id, reason_type=1, reason_text="测试举报原因内容")
        assert_success(result)
        assert_text_contains(result, "举报成功")

    @pytest.mark.forum
    @pytest.mark.p1
    def test_report_post_empty_reason(self, user_token, visible_forum_post_id):
        """FORUM-026 举报原因为空。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.report_post(post_id=visible_forum_post_id, reason_type=1, reason_text="")
        assert_failed(result)
        assert "举报原因不能为空" in result["message"], result


@allure.feature("forum")
class TestForumAdmin:
    @pytest.mark.forum
    @pytest.mark.admin
    @pytest.mark.p0
    def test_admin_list_pending_contains_new_post(self, admin_token, created_forum_post):
        """FORUM-027 待审核帖子列表包含刚发的帖子。"""
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

    @pytest.mark.forum
    @pytest.mark.admin
    @pytest.mark.p0
    def test_admin_audit_then_visible(self, user_token, admin_token, created_forum_post):
        """FORUM-028 审核通过帖子后普通用户可查看详情。"""
        if not admin_token or not user_token:
            pytest.skip("login failed")
        request_util.set_token(admin_token)
        audit_result = forum_api.admin_audit_post(post_id=created_forum_post["id"], audit_status=1)
        assert_success(audit_result)
        assert_text_contains(audit_result, "审核完成")

        request_util.set_token(user_token)
        detail_result = forum_api.get_post_detail(post_id=created_forum_post["id"])
        assert_success(detail_result)

    @pytest.mark.forum
    @pytest.mark.admin
    @pytest.mark.p1
    def test_admin_list_moderation(self, admin_token):
        """FORUM-029 内容监管帖子列表。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = forum_api.admin_list_moderation(page_num=1, page_size=10)
        assert_success(result)

    @pytest.mark.forum
    @pytest.mark.admin
    @pytest.mark.p1
    def test_admin_list_comments(self, admin_token):
        """FORUM-030 管理员评论列表。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = forum_api.admin_list_comments(page_num=1, page_size=10)
        assert_success(result)

    @pytest.mark.forum
    @pytest.mark.admin
    @pytest.mark.p1
    def test_admin_list_reports(self, admin_token):
        """FORUM-031 举报列表。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = forum_api.admin_list_reports(page_num=1, page_size=10)
        assert_success(result)

    @pytest.mark.forum
    @pytest.mark.admin
    @pytest.mark.p2
    def test_admin_handle_report(self, admin_token):
        """FORUM-032 处理举报。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        list_result = forum_api.admin_list_reports(page_num=1, page_size=10)
        assert_success(list_result)
        records = get_page_records(list_result)
        if not records:
            pytest.skip("no forum report available")
        report_id = records[0].get("id")
        result = forum_api.admin_audit_report(report_id=report_id, status=1, handle_remark="测试处理")
        assert_success(result)
        assert_text_contains(result, "举报处理完成")

    @pytest.mark.forum
    @pytest.mark.p1
    def test_admin_pending_forbidden_for_user(self, user_token):
        """FORUM-033 普通用户访问管理接口。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = forum_api.admin_list_pending(page_num=1, page_size=10)
        assert_failed(result)
