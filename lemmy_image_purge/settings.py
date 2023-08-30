"""Settings for Lemmy Image Purge."""
import sys

from loguru import logger
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for Lemmy Image Purge."""

    database_url: str
    pictrs_url: str
    pictrs_api_key: str


settings = Settings()

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>"
)
logger.remove()
logger.add(sys.stdout, format=logger_format)
