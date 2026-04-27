import logging_bullet_train as lbt
from tests._helpers import ANSI_RE, stream_logger


def test_color_false_removes_ansi_codes():
    stream, logger = stream_logger("tests.no_color")

    lbt.set_logger(logger, stream=stream, color=False)
    logger.info("plain")

    assert not ANSI_RE.search(stream.getvalue())
