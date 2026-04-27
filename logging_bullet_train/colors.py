"""Color helpers for bullet-train log output."""

import logging
import typing

from colorama import Back, Fore, Style

from logging_bullet_train.themes import LOGGING_UNKNOWN

BACK_ARROW: typing.TypeAlias = tuple[str | None, str | None]
ColorMode: typing.TypeAlias = typing.Literal["auto", "always", "never"] | bool

datetime_color: BACK_ARROW = (Back.WHITE, Fore.WHITE)
levelname_color: dict[int, BACK_ARROW] = {
    logging.DEBUG: (Back.BLUE, Fore.BLUE),
    logging.INFO: (Back.GREEN, Fore.GREEN),
    logging.WARNING: (Back.YELLOW, Fore.YELLOW),
    logging.ERROR: (Back.RED, Fore.RED),
    logging.CRITICAL: (Back.MAGENTA, Fore.MAGENTA),
    LOGGING_UNKNOWN: (Back.BLACK, Fore.BLACK),
}
logger_name_color: dict[int, BACK_ARROW] = {
    logging.DEBUG: (Back.LIGHTBLUE_EX, Fore.LIGHTBLUE_EX),
    logging.INFO: (Back.LIGHTGREEN_EX, Fore.LIGHTGREEN_EX),
    logging.WARNING: (Back.LIGHTYELLOW_EX, Fore.LIGHTYELLOW_EX),
    logging.ERROR: (Back.LIGHTRED_EX, Fore.LIGHTRED_EX),
    logging.CRITICAL: (Back.LIGHTMAGENTA_EX, Fore.LIGHTMAGENTA_EX),
    LOGGING_UNKNOWN: (Back.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX),
}
msg_color: dict[int, str | None] = {
    logging.DEBUG: None,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA,
    LOGGING_UNKNOWN: None,
}


def use_color(mode: ColorMode, stream: typing.Any = None) -> bool:
    """Resolve a color mode to a concrete boolean."""
    if isinstance(mode, bool):
        return mode
    if mode == "always":
        return True
    if mode == "never":
        return False
    if mode != "auto":
        raise ValueError("color must be True, False, 'auto', 'always', or 'never'")

    import os

    if os.getenv("NO_COLOR"):
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


def wrap_text(
    text: str,
    *,
    fg: str | None = None,
    bg: str | None = None,
    color: bool = True,
) -> str:
    """Wrap text with colorama color codes when color is enabled."""
    if not color:
        return text

    fg_str = fg or ""
    bg_str = bg or ""
    return f"{bg_str}{fg_str}{text}{Style.RESET_ALL}"
