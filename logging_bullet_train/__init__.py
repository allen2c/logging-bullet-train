"""Bullet-train style utilities for Python logging."""

import logging

from colorama import Back, Fore, Style

from logging_bullet_train.colors import (
    datetime_color,
    levelname_color,
    logger_name_color,
    msg_color,
    use_color,
    wrap_text,
)
from logging_bullet_train.formatters import (
    BulletTrainFormatter,
    IsoDatetimeFormatter,
    resolve_timezone,
    to_level,
)
from logging_bullet_train.logger import set_logger
from logging_bullet_train.themes import (
    LOGGING_UNKNOWN,
    get_theme,
    level_emoji_default,
    level_emoji_fruit,
    level_emoji_night,
    level_emoji_weather,
    level_emojis,
)
from logging_bullet_train.version import VERSION

__version__ = VERSION
__all__ = [
    "Back",
    "BulletTrainFormatter",
    "Fore",
    "IsoDatetimeFormatter",
    "LOGGING_UNKNOWN",
    "Style",
    "VERSION",
    "__version__",
    "datetime_color",
    "get_theme",
    "level_emoji_default",
    "level_emoji_fruit",
    "level_emoji_night",
    "level_emoji_weather",
    "level_emojis",
    "levelname_color",
    "logger_name_color",
    "msg_color",
    "resolve_timezone",
    "set_logger",
    "to_level",
    "use_color",
    "wrap_text",
]

logging.addLevelName(LOGGING_UNKNOWN, "UNKNOWN")
