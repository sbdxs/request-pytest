"""Home & file upload API tests — 对应 接口测试用例/06-首页与文件上传用例.md (HOME-001, FILE-001 ~ FILE-010)."""

from __future__ import annotations

import allure
import pytest

from api.home_api import home_api
from api.user_api import user_api
from conftest import assert_failed, assert_success
from utils.request_util import request_util


@pytest.fixture(scope="module")
def uploaded_png(upload_file_factory):
    return upload_file_factory("test.png")


@allure.feature("home")
class TestHome:
    @pytest.mark.home
    @pytest.mark.p0
    def test_get_hot_content(self, user_token):
        """HOME-001 获取首页热点内容（实测该接口需要登录态）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = home_api.get_hot_content()
        assert_success(result)
        assert result["data"], result


@allure.feature("upload")
class TestFileUploadSingle:
    @pytest.mark.upload
    @pytest.mark.p0
    def test_upload_avatar(self, user_token, upload_file_factory):
        """FILE-001 上传头像成功。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        jpg_path = upload_file_factory("test.jpg")
        result = user_api.upload_avatar(jpg_path)
        assert_success(result)
        assert str(result["data"]).startswith("/upload/avatar/"), result

    @pytest.mark.upload
    @pytest.mark.p1
    def test_upload_non_image(self, user_token, upload_file_factory):
        """FILE-002 上传非图片文件。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        txt_path = upload_file_factory("test.txt", content="plain text".encode())
        result = user_api.upload_avatar(txt_path)
        assert_failed(result)
        assert "仅支持图片格式" in result["message"], result

    @pytest.mark.upload
    @pytest.mark.p1
    def test_upload_empty_file(self, user_token, upload_file_factory):
        """FILE-003 上传空文件。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        empty_path = upload_file_factory("empty.jpg", content=b"")
        result = user_api.upload_avatar(empty_path)
        assert_failed(result)
        assert "请选择图片" in result["message"], result

    @pytest.mark.upload
    @pytest.mark.p2
    def test_upload_file_without_extension(self, user_token, upload_file_factory):
        """FILE-004 无扩展名文件。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        noext_path = upload_file_factory("noext")
        result = user_api.upload_avatar(noext_path)
        assert_failed(result)
        assert "文件没有扩展名" in result["message"], result

    @pytest.mark.upload
    @pytest.mark.admin
    @pytest.mark.p2
    def test_upload_news_image(self, admin_token, uploaded_png):
        """FILE-005 上传新闻图片（管理员）。"""
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = user_api.upload_news_image(uploaded_png)
        assert_success(result)
        assert str(result["data"]).startswith("/upload/news/"), result

    @pytest.mark.upload
    @pytest.mark.p2
    def test_upload_lost_found_image(self, user_token, uploaded_png):
        """FILE-006 上传失物图片。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = user_api.upload_lost_found_image(uploaded_png)
        assert_success(result)
        assert str(result["data"]).startswith("/upload/lost-found/"), result


@allure.feature("upload")
class TestFileUploadMultiple:
    @pytest.mark.upload
    @pytest.mark.p2
    def test_upload_lost_found_multiple(self, user_token, upload_file_factory):
        """FILE-007 批量上传失物图片（2张）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        files = [upload_file_factory(f"lf_{i}.jpg") for i in range(2)]
        result = user_api.upload_lost_found_multiple(files)
        assert_success(result)
        assert isinstance(result["data"], list) and len(result["data"]) == 2, result

    @pytest.mark.upload
    @pytest.mark.p2
    def test_upload_lost_found_multiple_over_limit(self, user_token, upload_file_factory):
        """FILE-008 批量上传超限（10张，上限9）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        files = [upload_file_factory(f"over_{i}.jpg") for i in range(10)]
        result = user_api.upload_lost_found_multiple(files)
        assert_failed(result)
        assert "最多上传9张图片" in result["message"], result

    @pytest.mark.upload
    @pytest.mark.p2
    def test_upload_forum_multiple(self, user_token, upload_file_factory):
        """FILE-009 批量上传论坛图片。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        files = [upload_file_factory(f"forum_{i}.png") for i in range(2)]
        result = user_api.upload_forum_multiple(files)
        assert_success(result)
        assert isinstance(result["data"], list), result
        for path in result["data"]:
            assert str(path).startswith("/upload/forum/"), result

    @pytest.mark.upload
    @pytest.mark.p2
    def test_upload_multiple_empty_list(self, user_token):
        """FILE-010 批量上传空文件列表（后端以 multipart 缺失校验返回 400）。"""
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = user_api.upload_lost_found_multiple([])
        assert_failed(result)
        assert result["code"] == 400, result
