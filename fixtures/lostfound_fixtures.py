"""失物招领模块夹具：招领数据与审核前置。"""

from __future__ import annotations

import pytest

from api.lostfound_api import lostfound_api
from fixtures.helpers import LOST_FOUND_AUDIT_APPROVED, assert_success
from utils.data_util import data_util
from utils.request_util import request_util


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
