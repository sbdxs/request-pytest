"""即时消息模块夹具：私信内容数据。"""

from __future__ import annotations

import pytest

from utils.data_util import data_util


@pytest.fixture
def im_message_data():
    return {"content": data_util.generate_content(paragraphs=1)}
