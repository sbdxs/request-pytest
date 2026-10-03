"""跨模块共享的断言助手与测试数据构造工具。"""

from __future__ import annotations

FORUM_AUDIT_APPROVED = 1
LOST_FOUND_AUDIT_APPROVED = 1


def assert_success(result: dict, *, status_code: int = 200) -> None:
    assert result["status_code"] == status_code, result
    assert result["success"] is True, result
    assert result["code"] == 200, result


def assert_failed(result: dict, *, status_code: int | None = None) -> None:
    assert result["success"] is False, result
    if status_code is not None:
        assert result["status_code"] == status_code, result
    assert result["code"] != 200, result


def result_text(result: dict) -> str:
    """拼接 message 与 data，兼容后端把业务提示放在 data 字段的接口。"""
    message = result.get("message") or ""
    data = result.get("data")
    if isinstance(data, str):
        return f"{message}{data}"
    return message


def assert_text_contains(result: dict, text: str) -> None:
    assert text in result_text(result), result


def get_page_records(result: dict) -> list[dict]:
    data = result.get("data") or {}
    return data.get("records") or []


def _digits_only(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    return digits or "0"


def build_unique_student_id(seed: str) -> str:
    digits = _digits_only(seed)
    return digits[-10:].rjust(10, "0")


def build_unique_phone(seed: str) -> str:
    digits = _digits_only(seed)
    return f"13{digits[-9:].rjust(9, '0')}"
