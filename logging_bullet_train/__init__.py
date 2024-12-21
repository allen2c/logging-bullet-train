import datetime
import logging
import os
import typing
import zoneinfo

from colorama import Back, Fore, Style

levelname_bg = {
    "DEBUG": Back.BLUE,
    "INFO": Back.GREEN,
    "WARNING": Back.YELLOW,
    "ERROR": Back.RED,
    "CRITICAL": Back.RED,
}
message_fg = {
    "DEBUG": Fore.BLUE,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.RED,
}
bg2fg = {
    Back.BLACK: Fore.BLACK,
    Back.RED: Fore.RED,
    Back.GREEN: Fore.GREEN,
    Back.YELLOW: Fore.YELLOW,
    Back.BLUE: Fore.BLUE,
    Back.MAGENTA: Fore.MAGENTA,
    Back.CYAN: Fore.CYAN,
    Back.WHITE: Fore.WHITE,
    Back.RESET: Fore.WHITE,
    Back.LIGHTBLACK_EX: Fore.WHITE,
    Back.LIGHTRED_EX: Fore.WHITE,
    Back.LIGHTGREEN_EX: Fore.BLACK,
    Back.LIGHTYELLOW_EX: Fore.BLACK,
    Back.LIGHTBLUE_EX: Fore.WHITE,
    Back.LIGHTMAGENTA_EX: Fore.WHITE,
    Back.LIGHTCYAN_EX: Fore.BLACK,
    Back.LIGHTWHITE_EX: Fore.BLACK,
}


def bg_to_fg(bg: typing.Text) -> typing.Text:
    return {
        Back.BLACK: Fore.WHITE,
        Back.RED: Fore.WHITE,
        Back.GREEN: Fore.BLACK,
        Back.YELLOW: Fore.BLACK,
        Back.BLUE: Fore.WHITE,
        Back.MAGENTA: Fore.WHITE,
        Back.CYAN: Fore.BLACK,
        Back.WHITE: Fore.BLACK,
        Back.RESET: Fore.WHITE,
        Back.LIGHTBLACK_EX: Fore.WHITE,
        Back.LIGHTRED_EX: Fore.WHITE,
        Back.LIGHTGREEN_EX: Fore.BLACK,
        Back.LIGHTYELLOW_EX: Fore.BLACK,
        Back.LIGHTBLUE_EX: Fore.WHITE,
        Back.LIGHTMAGENTA_EX: Fore.WHITE,
        Back.LIGHTCYAN_EX: Fore.BLACK,
        Back.LIGHTWHITE_EX: Fore.BLACK,
    }[bg]


class IsoDatetimeFormatter(logging.Formatter):
    def formatTime(
        self, record: logging.LogRecord, datefmt: typing.Literal[None] = None
    ):
        record_datetime = datetime.datetime.fromtimestamp(record.created).astimezone(
            zoneinfo.ZoneInfo(os.getenv("TZ") or "UTC")
        )
        # Drop microseconds
        record_datetime = record_datetime.replace(microsecond=0)
        return record_datetime.isoformat()


class ColoredIsoDatetimeFormatter(IsoDatetimeFormatter):
    def format(self, record: logging.LogRecord):
        arrow = "\uE0B0"
        level_bg = levelname_bg.get(record.levelname, Back.BLACK)
        msg_fg = message_fg.get(record.levelname, Fore.WHITE)

        ts = self.formatTime(record)
        time_colored = (
            f"{Back.WHITE}{Fore.BLACK} {ts} {Style.RESET_ALL}"
            + f"{level_bg}{Fore.WHITE}{arrow}{Style.RESET_ALL}"
        )
        level_colored = (
            f"{level_bg} {record.levelname:8s} {Style.RESET_ALL}"
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


def bullet_train_style_prompt():
    # Directory section
    directory = Style.BRIGHT + Back.BLUE + Fore.WHITE + " ~/Documents "
    directory_arrow_separator = Style.RESET_ALL + Back.GREEN + Fore.BLUE + "\uE0B0"

    # Git status section
    git_status = Style.RESET_ALL + Back.GREEN + Fore.BLACK + " main ✔ "
    git_status_arrow_separator = Style.RESET_ALL + Back.YELLOW + Fore.GREEN + "\uE0B0"
    # Python version section
    python_section = Style.RESET_ALL + Back.YELLOW + Fore.BLACK + " 🐍 3.9.0 "
    python_section_arrow_separator = (
        Style.RESET_ALL + Back.WHITE + Fore.YELLOW + "\uE0B0"
    )

    # Time section
    time_section = Style.RESET_ALL + Back.WHITE + Fore.BLACK + " ⌚ 14:00 "
    time_section_arrow_separator = Style.RESET_ALL + Fore.WHITE + "\uE0B0"

    # Print the prompt
    print(
        directory
        + directory_arrow_separator
        + git_status
        + git_status_arrow_separator
        + python_section
        + python_section_arrow_separator
        + time_section
        + time_section_arrow_separator
        + Style.RESET_ALL
    )
    print(Fore.CYAN + "➜ ", end="")


def set_logger(
    logger: logging.Logger | typing.Text, *, level: int = logging.DEBUG
) -> logging.Logger:
    logger = logging.getLogger(logger) if isinstance(logger, typing.Text) else logger

    # Remove all handlers of logger
    logger.handlers = []

    # Add a stream handler
    handler = logging.StreamHandler()

    # Set the formatter
    handler.setFormatter(ColoredIsoDatetimeFormatter())

    # Set the level
    handler.setLevel(level)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    logger = set_logger("sdk")
    logger.setLevel(logging.DEBUG)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
