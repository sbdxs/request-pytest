"""Base API wrapper."""

from __future__ import annotations

from typing import Any

from loguru import logger

from utils.request_util import request_util


class BaseAPI:
    def __init__(self) -> None:
        self.request = request_util

    def _handle_response(self, response: Any) -> dict[str, Any]:
        try:
            result = response.json()
        except Exception as exc:
            logger.error("failed to parse response json: {}", exc)
            return {
                "status_code": response.status_code,
                "code": None,
                "message": str(exc),
                "data": None,
                "success": False,
                "raw": response.text[:2000],
            }

        return {
            "status_code": response.status_code,
            "code": result.get("code"),
            "message": result.get("message", ""),
            "data": result.get("data"),
            "success": result.get("code") == 200,
            "raw": result,
        }

    def _get(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._handle_response(self.request.get(url, params=params))

    def _post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._handle_response(self.request.post(url, data=data, json=json))

    def _put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._handle_response(self.request.put(url, data=data, json=json))

    def _delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._handle_response(self.request.delete(url, params=params, json=json, data=data))

    def _patch(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._handle_response(self.request.patch(url, data=data, json=json))
