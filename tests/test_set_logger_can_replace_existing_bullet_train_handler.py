import io

import logging_bullet_train as lbt
from tests._helpers import stream_logger


def test_set_logger_can_replace_existing_bullet_train_handler():
    first_stream, logger = stream_logger("tests.replace")
    second_stream = io.StringIO()

    lbt.set_logger(logger, stream=first_stream, color=False)
    lbt.set_logger(logger, stream=second_stream, color=False, replace_handlers=True)
    logger.warning("moved")

    assert first_stream.getvalue() == ""
    assert "moved" in second_stream.getvalue()
    assert len(logger.handlers) == 1
