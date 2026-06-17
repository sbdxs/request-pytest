"""HTTP request helper used by the local API tests."""

from __future__ import annotations

import json
from typing import Any

import requests
from loguru import logger

from config.config import config


class RequestUtil:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.base_url = config.base_url.rstrip("/")
        self.timeout = config.timeout
        self.token: str | None = None
        self.last_request: dict[str, Any] | None = None
        self.last_response: dict[str, Any] | None = None

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        kwargs.setdefault("timeout", self.timeout)

        request_snapshot = self._build_request_snapshot(method=method, url=full_url, kwargs=kwargs)
        self.last_request = request_snapshot
        self.last_response = None

        logger.info("request {} {}", method.upper(), full_url)
        try:
            response = self.session.request(method, full_url, **kwargs)
        except requests.RequestException as exc:
            logger.error("request failed: {}", exc)
            self.last_response = {"error": str(exc)}
            raise

        self.last_response = self._build_response_snapshot(response)
        logger.info("response {} {}", response.status_code, full_url)
        try:
            logger.debug("response body: {}", response.json())
        except Exception:
            logger.debug("response text: {}", response.text[:500])
        return response

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", url, **kwargs)

    def set_headers(self, headers: dict[str, str]) -> None:
        self.session.headers.update(headers)

    def set_token(self, token: str | None) -> None:
        self.token = token
        if not token:
            self.clear_token()
            return

        auth_value = token if token.startswith("Bearer ") else f"Bearer {token}"
        self.session.headers.update({"Authorization": auth_value})
        logger.info("authorization header set")

    def set_token_raw(self, token: str | None) -> None:
        self.token = token
        if token:
            self.session.headers.update({"Authorization": token})

    def get_token(self) -> str | None:
        return self.token

    def clear_headers(self) -> None:
        self.session.headers.clear()
        self.token = None
        self.last_request = None
        self.last_response = None

    def clear_token(self) -> None:
        self.session.headers.pop("Authorization", None)
        self.token = None

    def get_last_exchange(self) -> dict[str, Any]:
        return {
            "request": self.last_request,
            "response": self.last_response,
        }

    def _build_request_snapshot(self, method: str, url: str, kwargs: dict[str, Any]) -> dict[str, Any]:
        snapshot = {
            "method": method.upper(),
            "url": url,
            "headers": self._sanitize_headers(dict(self.session.headers)),
        }
        if "params" in kwargs and kwargs["params"] is not None:
            snapshot["params"] = kwargs["params"]
        if "json" in kwargs and kwargs["json"] is not None:
            snapshot["json"] = kwargs["json"]
        if "data" in kwargs and kwargs["data"] is not None:
            snapshot["data"] = kwargs["data"]
        if "timeout" in kwargs:
            snapshot["timeout"] = kwargs["timeout"]
        return snapshot

    def _build_response_snapshot(self, response: requests.Response) -> dict[str, Any]:
        body: Any
        try:
            body = response.json()
        except Exception:
            body = response.text[:2000]
        return {
            "status_code": response.status_code,
            "headers": self._sanitize_headers(dict(response.headers)),
            "body": body,
        }

    def _sanitize_headers(self, headers: dict[str, Any]) -> dict[str, Any]:
        sanitized = {}
        for key, value in headers.items():
            if key.lower() == "authorization" and isinstance(value, str):
                sanitized[key] = self._mask_token(value)
            else:
                sanitized[key] = value
        return sanitized

    def _mask_token(self, token_value: str) -> str:
        if len(token_value) <= 16:
            return "***"
        return f"{token_value[:10]}...{token_value[-6:]}"

    def dump_last_exchange(self) -> str:
        return json.dumps(self.get_last_exchange(), ensure_ascii=False, indent=2, default=str)


request_util = RequestUtil()
