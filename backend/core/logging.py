import sys
from typing import Literal, TypeAlias

import loguru
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = loguru.logger

LogLevel: TypeAlias = Literal[
    'TRACE',
    'DEBUG',
    'INFO',
    'SUCCESS',
    'WARNING',
    'ERROR',
    'CRITICAL',
]


class LogSettings(BaseSettings):
    LOG_LEVEL: LogLevel = 'DEBUG'
    LOG_FILE: str = '.logs/app.log'
    LOG_FILE_ROTATION: str = '10 MB'
    LOG_FILE_RETENTION: str = '30 days'
    LOG_FILE_COMPRESSION: str = 'zip'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


log_settings = LogSettings()


def configure_logging() -> None:
    logger.remove()

    logger.add(
        sink=sys.stdout,
        format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
        '<level>{level}</level> | '
        '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
        '<level>{message}</level>',
        level=log_settings.LOG_LEVEL,
        colorize=True,
    )

    logger.add(
        sink=log_settings.LOG_FILE,
        rotation=log_settings.LOG_FILE_ROTATION,
        retention=log_settings.LOG_FILE_RETENTION,
        compression=log_settings.LOG_FILE_COMPRESSION,
        format='{time:YYYY-MM-DD HH:mm:ss.SSS} | '
        '{level} | '
        '{name}:{function}:{line} - {message}',
        level=log_settings.LOG_LEVEL,
        enqueue=True,
    )

    logger.level(log_settings.LOG_LEVEL)
