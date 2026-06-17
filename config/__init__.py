"""Configuration package exports."""

from .config import Config, config


def get_config(env: str = "dev") -> Config:
    return config


__all__ = ["Config", "config", "get_config"]
