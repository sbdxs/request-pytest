"""Test configuration for the local API suite."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    base_url: str = os.getenv("BASE_URL", "http://localhost:8080")
    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "123456")
    test_user_username: str = os.getenv("TEST_USER_USERNAME", "stu_zhang")
    test_user_password: str = os.getenv("TEST_USER_PASSWORD", "123456")
    timeout: int = int(os.getenv("TIMEOUT", "10"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))

    @property
    def test_data_dir(self) -> str:
        return str(Path(__file__).resolve().parent.parent / "data")

    @property
    def report_dir(self) -> str:
        return str(Path(__file__).resolve().parent.parent / "report")


config = Config()
