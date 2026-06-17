"""Home API tests."""

from __future__ import annotations

import allure
import pytest

from api.home_api import home_api
from conftest import assert_success
from utils.request_util import request_util


@allure.feature("home")
class TestHome:
    @pytest.mark.home
    def test_get_hot_content(self, user_token):
        if not user_token:
            pytest.skip("user login failed")
        request_util.set_token(user_token)
        result = home_api.get_hot_content()
        assert_success(result)
        assert result["data"] is not None
