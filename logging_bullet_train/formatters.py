"""Formatters for bullet-train log output."""

import datetime
import logging
import os
import typing
import zoneinfo

from colorama import Style

from logging_bullet_train.colors import (
    ColorMode,
    datetime_color,
    levelname_color,
    logger_name_color,
    msg_color,
    use_color,
    wrap_text,
)
from logging_bullet_train.themes import LOGGING_UNKNOWN, Theme, get_theme

Level: typing.TypeAlias = typing.Literal[1, 10, 20, 30, 40, 50]
Timezone: typing.TypeAlias = str | datetime.tzinfo | None
_LEVELS: tuple[Level, ...] = (
    LOGGING_UNKNOWN,  # type: ignore[list-item]
    logging.DEBUG,  # type: ignore[list-item]
    logging.INFO,  # type: ignore[list-item]
    logging.WARNING,  # type: ignore[list-item]
    logging.ERROR,  # type: ignore[list-item]
    logging.CRITICAL,  # type: ignore[list-item]
)


def to_level(levelname: str | int) -> Level:
    """Normalize a logging level name or value to a styled level."""
    if isinstance(levelname, str):
        return _level_from_name(levelname)

    if levelname >= logging.CRITICAL:
        return logging.CRITICAL  # type: ignore[return-value]
    if levelname >= logging.ERROR:
        return logging.ERROR  # type: ignore[return-value]
    if levelname >= logging.WARNING:
        return logging.WARNING  # type: ignore[return-value]
    if levelname >= logging.INFO:
        return logging.INFO  # type: ignore[return-value]
    if levelname >= logging.DEBUG:
        return logging.DEBUG  # type: ignore[return-value]
    return LOGGING_UNKNOWN  # type: ignore[return-value]


class IsoDatetimeFormatter(logging.Formatter):
    """Logging formatter with ISO-8601 timestamps."""

    def __init__(
        self,
        *args: typing.Any,
        timezone: Timezone = None,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.timezone = resolve_timezone(timezone)

    def formatTime(
        self,
        record: logging.LogRecord,
        datefmt: str | None = None,
    ) -> str:
        record_datetime = datetime.datetime.fromtimestamp(
            record.created,
            tz=self.timezone,
        ).replace(microsecond=0)
        return record_datetime.isoformat()


class BulletTrainFormatter(IsoDatetimeFormatter):
    """Colorful bullet-train formatter for standard library logging."""

    arrow = "\ue0b0"

    def __init__(
        self,
        *args: typing.Any,
        theme: str | Theme = "default",
        color: ColorMode = "auto",
        stream: typing.Any = None,
        show_datetime: bool = True,
        show_level: bool = True,
        show_logger_name: bool = True,
        show_lineno: bool = True,
        show_message: bool = True,
        timezone: Timezone = None,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(*args, timezone=timezone, **kwargs)
        self.theme = get_theme(theme)
        self.color = use_color(color, stream)
        self.show_datetime = show_datetime
        self.show_level = show_level
        self.show_logger_name = show_logger_name
        self.show_lineno = show_lineno
        self.show_message = show_message
        self._last_timestamp_second: int | None = None
        self._last_timestamp_text = ""
        self._time_parts = self._build_time_parts()
        self._level_block_cache: dict[tuple[int, str], str] = {}
        self._logger_name_parts = self._build_logger_name_parts()
        self._message_style = self._build_message_styles()

    def format(self, record: logging.LogRecord) -> str:
        level = to_level(record.levelno)
        prefix = self._prefix(record, level)
        message = self._message(record, level)
        line = message.lstrip() if not prefix else prefix + message
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line

    def formatTime(
        self,
        record: logging.LogRecord,
        datefmt: str | None = None,
    ) -> str:
        second = int(record.created)
        if second != self._last_timestamp_second:
            self._last_timestamp_second = second
            self._last_timestamp_text = super().formatTime(record, datefmt)
        return self._last_timestamp_text

    def _prefix(self, record: logging.LogRecord, level: int) -> str:
        prefix = ""

        if self.show_datetime:
            left, right = self._time_parts[level]
            prefix += f"{left}{self.formatTime(record)}{right}"

        if self.show_level:
            prefix += self._level_block(level, record.levelname)

        if self.show_logger_name:
            name = record.name
            if self.show_lineno:
                name = f"{name}:{record.lineno}"
            left, right = self._logger_name_parts[level]
            prefix += f"{left}{name}{right}"

        return prefix

    def _message(self, record: logging.LogRecord, level: int) -> str:
        if not self.show_message:
            return ""
        message = record.getMessage()
        prefix, suffix = self._message_style[level]
        return f"{prefix}{message}{suffix}"

    def _build_message_styles(self) -> dict[int, tuple[str, str]]:
        styles = {}
        for level in _LEVELS:
            color = msg_color[level]
            if self.color and color:
                styles[level] = (f"{color} ", Style.RESET_ALL)
            else:
                styles[level] = (" ", "")
        return styles

    def _build_time_parts(self) -> dict[int, tuple[str, str]]:
        parts = {}
        if not self.show_datetime:
            return parts

        for level in _LEVELS:
            next_bg = levelname_color[level][0] if self.show_level else None
            if not next_bg and self.show_logger_name:
                next_bg = logger_name_color[level][0]
            parts[level] = self._block_parts(datetime_color, next_bg)
        return parts

    def _build_logger_name_parts(self) -> dict[int, tuple[str, str]]:
        if not self.show_logger_name:
            return {}
        return {
            level: self._block_parts(logger_name_color[level], None)
            for level in _LEVELS
        }

    def _level_block(self, level: int, levelname: str) -> str:
        key = (level, levelname)
        try:
            return self._level_block_cache[key]
        except KeyError:
            block = self._build_level_block(level, levelname)
            self._level_block_cache[key] = block
            return block

    def _build_level_block(self, level: int, levelname: str) -> str:
        levelname = f"{self.theme[level]} {levelname}"
        bg = levelname_color[level][0]
        fg = levelname_color[level][1]
        following_bg = logger_name_color[level][0] if self.show_logger_name else None
        return self._block(f" {levelname:10s} ", (bg, fg), following_bg)

    def _block(
        self,
        text: str,
        colors: tuple[str | None, str | None],
        next_bg: str | None,
    ) -> str:
        return self._wrap(text, bg=colors[0]) + self._wrap(
            self.arrow, fg=colors[1], bg=next_bg
        )

    def _block_parts(
        self,
        colors: tuple[str | None, str | None],
        next_bg: str | None,
    ) -> tuple[str, str]:
        if not self.color:
            return " ", f" {self.arrow}"

        bg, fg = colors
        arrow = self._wrap(self.arrow, fg=fg, bg=next_bg)
        return f"{bg or ''} ", f" {Style.RESET_ALL}{arrow}"

    def _wrap(
        self,
        text: str,
        *,
        fg: str | None = None,
        bg: str | None = None,
    ) -> str:
        return wrap_text(text, fg=fg, bg=bg, color=self.color)


def resolve_timezone(timezone: Timezone = None) -> datetime.tzinfo:
    """Resolve a timezone using only the standard library."""
    if isinstance(timezone, datetime.tzinfo):
        return timezone
    if timezone:
        return zoneinfo.ZoneInfo(timezone)

    tz_env = os.getenv("TZ")
    if tz_env and tz_env.strip():
        try:
            return zoneinfo.ZoneInfo(tz_env.strip())
        except zoneinfo.ZoneInfoNotFoundError:
            pass

    return zoneinfo.ZoneInfo("UTC")


def _level_from_name(levelname: str) -> Level:
    level = logging.getLevelNamesMapping().get(levelname.upper())
    if isinstance(level, int):
        return to_level(level)
    return LOGGING_UNKNOWN  # type: ignore[return-value]
