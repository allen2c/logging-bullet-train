import logging_bullet_train as lbt
from tests._helpers import stream_logger


def test_set_logger_writes_once_without_duplicate_handlers():
    stream, logger = stream_logger("tests.once")

    lbt.set_logger(logger, stream=stream, color=False, propagate=False)
    lbt.set_logger(logger, stream=stream, color=False, propagate=False)
    logger.info("hello")

    assert stream.getvalue().count("hello") == 1
    assert len(logger.handlers) == 1
    assert logger.propagate is False
