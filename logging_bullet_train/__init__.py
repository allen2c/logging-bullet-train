import datetime
import logging
import os
import typing
import zoneinfo

import tzlocal
from colorama import Back, Fore, Style

level_emoji_default = {
    "DEBUG": "🔎",
    "INFO": "💡",
    "WARNING": "⭐",
    "ERROR": "🚨",
    "CRITICAL": "🔥",
    "NOTSET": "🔘",
}
level_emoji_fruit = {
    "DEBUG": "🫐",
    "INFO": "🍏",
    "WARNING": "🍋",
    "ERROR": "🍒",
    "CRITICAL": "🌶️",
    "NOTSET": "🍇",
}
level_emoji_weather = {
    "DEBUG": "🌤️",
    "INFO": "☀️",
    "WARNING": "🌦️",
    "ERROR": "⛈️",
    "CRITICAL": "🌪️",
    "NOTSET": "🌈",
}
level_emoji_night = {
    "DEBUG": "🌑",
    "INFO": "🌓",
    "WARNING": "🌕",
    "ERROR": "🌠",
    "CRITICAL": "☄️",
    "NOTSET": "🌌",
}
level_emojis = {
    "default": level_emoji_default,
    "fruit": level_emoji_fruit,
    "weather": level_emoji_weather,
    "night": level_emoji_night,
}


type BACK_ARROW = typing.Tuple[typing.Text | None, typing.Text | None]

datetime_color: BACK_ARROW = (Back.WHITE, Fore.WHITE)
levelname_color: typing.Dict[typing.Text, BACK_ARROW] = {
    "DEBUG": (Back.BLUE, Fore.BLUE),
    "INFO": (Back.GREEN, Fore.GREEN),
    "WARNING": (Back.YELLOW, Fore.YELLOW),
    "ERROR": (Back.RED, Fore.RED),
    "CRITICAL": (Back.MAGENTA, Fore.MAGENTA),
    "NOTSET": (Back.BLACK, Fore.BLACK),
}
logger_name_color: typing.Dict[typing.Text, BACK_ARROW] = {
    "DEBUG": (Back.LIGHTBLUE_EX, Fore.LIGHTBLUE_EX),
    "INFO": (Back.LIGHTGREEN_EX, Fore.LIGHTGREEN_EX),
    "WARNING": (Back.LIGHTYELLOW_EX, Fore.LIGHTYELLOW_EX),
    "ERROR": (Back.LIGHTRED_EX, Fore.LIGHTRED_EX),
    "CRITICAL": (Back.LIGHTMAGENTA_EX, Fore.LIGHTMAGENTA_EX),
    "NOTSET": (Back.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX),
}
msg_color: typing.Dict[typing.Text, typing.Text | None] = {
    "DEBUG": None,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA,
    "NOTSET": None,
}


def wrap_text(
    text: typing.Text, fg: typing.Text = "", bg: typing.Text = ""
) -> typing.Text:
    return f"{bg}{fg}{text}{Style.RESET_ALL}"


class IsoDatetimeFormatter(logging.Formatter):
    def formatTime(
        self, record: logging.LogRecord, datefmt: typing.Literal[None] = None
    ):
        try:
            if (TZ_ := os.getenv("TZ")) and TZ_.strip():
                local_tz = zoneinfo.ZoneInfo(TZ_)
            else:
                local_tz = tzlocal.get_localzone()
        except Exception:
            local_tz = zoneinfo.ZoneInfo("UTC")
        record_datetime = datetime.datetime.fromtimestamp(record.created).astimezone(
            local_tz
        )
        # Drop microseconds
        record_datetime = record_datetime.replace(microsecond=0)
        return record_datetime.isoformat()


class BulletTrainFormatter(IsoDatetimeFormatter):
    def format(self, record: logging.LogRecord):
        arrow = "\uE0B0"
        level_bg = levelname_bg.get(record.levelname, Back.BLACK)
        level_emoji = levelname_emoji.get(record.levelname, "")
        msg_fg = message_fg.get(record.levelname, Fore.WHITE)

        ts = self.formatTime(record)
        time_colored = (
            f"{Back.WHITE}{Fore.BLACK} {ts} {Style.RESET_ALL}"
            + f"{level_bg}{Fore.WHITE}{arrow}{Style.RESET_ALL}"
        )
        level_colored = (
            f"{level_bg} {level_emoji} {record.levelname:8s} {Style.RESET_ALL}"
            + f"{Back.CYAN}{bg2fg[level_bg]}{arrow}{Style.RESET_ALL}"
        )
        name_colored = (
            f"{Back.CYAN} {record.name} {Style.RESET_ALL}"
            + f"{bg2fg[Back.CYAN]}{arrow}{Style.RESET_ALL}"
        )
        message_colored = f"{msg_fg} {record.getMessage()}{Style.RESET_ALL}"
        if record.exc_info:
            message_colored += "\n" + self.formatException(record.exc_info)

        # Output the log line
        log_line = f"{time_colored}{level_colored}{name_colored}{message_colored}"
        return log_line


def set_logger(
    logger: logging.Logger | typing.Text,
    *,
    level: int = logging.DEBUG,
    fmt: typing.Text = "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
) -> logging.Logger:
    logger = logging.getLogger(logger) if isinstance(logger, typing.Text) else logger
    handler = logging.StreamHandler()
    formatter = BulletTrainFormatter(fmt=fmt)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


if __name__ == "__main__":
    logger = set_logger("sdk")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
