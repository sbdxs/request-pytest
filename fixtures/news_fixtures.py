"""新闻模块夹具：新闻数据与已发布新闻前置。"""

from __future__ import annotations

import pytest

from api.news_api import news_api
from fixtures.helpers import assert_success, get_page_records
from utils.data_util import data_util


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


@pytest.fixture(scope="session")
def published_news_id():
    result = news_api.list(page_num=1, page_size=5)
    assert_success(result)
    records = get_page_records(result)
    if not records:
        pytest.skip("no published news available")
    return records[0]["id"]
