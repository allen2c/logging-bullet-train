"""Logger setup helpers."""

import logging
import sys
import typing

from logging_bullet_train.colors import ColorMode
from logging_bullet_train.formatters import BulletTrainFormatter, Timezone
from logging_bullet_train.themes import Theme

Stream: typing.TypeAlias = typing.TextIO


def set_logger(
    logger: logging.Logger | str,
    *,
    level: int | str = logging.DEBUG,
    handler_level: int | str | None = None,
    theme: str | Theme = "default",
    color: ColorMode = "auto",
    stream: Stream | None = None,
    timezone: Timezone = None,
    show_datetime: bool = True,
    show_level: bool = True,
    show_logger_name: bool = True,
    show_lineno: bool = True,
    show_message: bool = True,
    propagate: bool | None = None,
    disabled: bool | None = None,
    replace_handlers: bool = False,
) -> logging.Logger:
    """Configure and return a standard library logger."""
    logger = logging.getLogger(logger) if isinstance(logger, str) else logger
    stream = stream or sys.stderr
    level_value = _coerce_logging_level(level)
    handler_level_value = _coerce_logging_level(
        level_value if handler_level is None else handler_level
    )

    if propagate is not None:
        logger.propagate = propagate
    if disabled is not None:
        logger.disabled = disabled

    handler = _find_bullet_train_handler(logger, stream)
    if replace_handlers:
        _remove_bullet_train_handlers(logger)
        handler = None

    if handler is None:
        handler = logging.StreamHandler(stream)
        logger.addHandler(handler)

    handler.setFormatter(
        BulletTrainFormatter(
            theme=theme,
            color=color,
            stream=stream,
            timezone=timezone,
            show_datetime=show_datetime,
            show_level=show_level,
            show_logger_name=show_logger_name,
            show_lineno=show_lineno,
            show_message=show_message,
        )
    )
    handler.setLevel(handler_level_value)
    logger.setLevel(level_value)
    return logger


def _coerce_logging_level(level: int | str) -> int:
    if isinstance(level, str):
        value = logging.getLevelNamesMapping().get(level.upper())
        if isinstance(value, int):
            return value
        raise ValueError(f"unknown logging level: {level!r}")
    return level


def _find_bullet_train_handler(
    logger: logging.Logger,
    stream: Stream,
) -> logging.StreamHandler | None:
    for handler in logger.handlers:
        if not _is_bullet_train_handler(handler):
            continue
        if getattr(handler, "stream", None) is stream:
            return typing.cast(logging.StreamHandler, handler)
    return None


def _remove_bullet_train_handlers(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        if _is_bullet_train_handler(handler):
            logger.removeHandler(handler)
            handler.close()


def _is_bullet_train_handler(handler: logging.Handler) -> bool:
    return isinstance(handler, logging.StreamHandler) and isinstance(
        handler.formatter,
        BulletTrainFormatter,
    )
