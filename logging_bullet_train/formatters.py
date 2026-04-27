"""Formatters for bullet-train log output."""

import datetime
import logging
import os
import typing
import zoneinfo

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

    def format(self, record: logging.LogRecord) -> str:
        level = to_level(record.levelno)
        blocks = self._blocks(record, level)
        message = self._message(record, level)

        line = message.lstrip() if not blocks else "".join(blocks) + message
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line

    def _blocks(self, record: logging.LogRecord, level: int) -> list[str]:
        blocks = []

        if self.show_datetime:
            next_bg = levelname_color[level][0] if self.show_level else None
            if not next_bg and self.show_logger_name:
                next_bg = logger_name_color[level][0]
            blocks.append(
                self._block(f" {self.formatTime(record)} ", datetime_color, next_bg)
            )

        if self.show_level:
            levelname = f"{self.theme[level]} {record.levelname}"
            bg = levelname_color[level][0]
            fg = levelname_color[level][1]
            following_bg = (
                logger_name_color[level][0] if self.show_logger_name else None
            )
            blocks.append(self._block(f" {levelname:10s} ", (bg, fg), following_bg))

        if self.show_logger_name:
            name = record.name
            if self.show_lineno:
                name = f"{name}:{record.lineno}"
            bg = logger_name_color[level][0]
            fg = logger_name_color[level][1]
            blocks.append(self._block(f" {name} ", (bg, fg), None))

        return blocks

    def _block(
        self,
        text: str,
        colors: tuple[str | None, str | None],
        next_bg: str | None,
    ) -> str:
        colored = wrap_text(text, bg=colors[0], color=self.color)
        arrow = wrap_text(self.arrow, fg=colors[1], bg=next_bg, color=self.color)
        return f"{colored}{arrow}"

    def _message(self, record: logging.LogRecord, level: int) -> str:
        if not self.show_message:
            return ""
        message = record.getMessage()
        return wrap_text(f" {message}", fg=msg_color[level], color=self.color)


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
