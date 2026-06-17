"""Lost and found API tests."""

from __future__ import annotations

import allure
import pytest

from api.lostfound_api import lostfound_api
from conftest import assert_success, get_page_records
from utils.request_util import request_util


@allure.feature("lostfound")
class TestLostFoundCreate:
    @pytest.mark.lostfound
    def test_create_lost(self, user_token, lostfound_data):
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
        data = result["data"]
        assert data["id"] is not None
        assert data["title"] == lostfound_data["title"]
        assert data["itemName"] == lostfound_data["itemName"]
        assert data["status"] == 3
        assert data["contactWay"] == 3
        assert data["isContactPublic"] == 0


@allure.feature("lostfound")
class TestLostFoundList:
    @pytest.mark.lostfound
    def test_list_all(self):
        result = lostfound_api.list(page_num=1, page_size=10)
        assert_success(result)
        assert result["data"] is not None
        assert "records" in result["data"]


@allure.feature("lostfound")
class TestLostFoundDetail:
    @pytest.mark.lostfound
    def test_get_detail(self, user_token, created_lost_found):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = lostfound_api.get_detail(lost_found_id=created_lost_found["id"])
        assert_success(result)
        data = result["data"]
        assert data["id"] == created_lost_found["id"]
        assert data["title"] == created_lost_found["title"]
        assert data["publisherId"] == created_lost_found["publisherId"]


@allure.feature("lostfound")
class TestLostFoundAdmin:
    @pytest.mark.lostfound
    def test_admin_list(self, admin_token, created_lost_found):
        if not admin_token:
            pytest.skip("admin login failed")
        request_util.set_token(admin_token)
        result = lostfound_api.admin_list(page_num=1, page_size=20)
        assert_success(result)
        records = get_page_records(result)
        assert any(record.get("id") == created_lost_found["id"] for record in records)

    @pytest.mark.lostfound
    def test_update_status_to_closed(self, user_token, approved_lost_found_id):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)

        update_result = lostfound_api.update_status(
            lost_found_id=approved_lost_found_id,
            status=2,
        )
        assert_success(update_result)

        detail_result = lostfound_api.get_detail(
            lost_found_id=approved_lost_found_id
        )
        assert_success(detail_result)
        assert detail_result["data"]["status"] == 2


