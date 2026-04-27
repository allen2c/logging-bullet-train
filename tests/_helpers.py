import io
import logging
import re

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


class TtyStringIO(io.StringIO):
    def isatty(self) -> bool:
        return True


def stream_logger(name: str) -> tuple[io.StringIO, logging.Logger]:
    stream = io.StringIO()
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = True
    logger.disabled = False
    return stream, logger
