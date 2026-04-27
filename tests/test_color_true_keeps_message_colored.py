import logging_bullet_train as lbt
from tests._helpers import stream_logger


def test_color_true_keeps_message_colored():
    stream, logger = stream_logger("tests.message_color")

    lbt.set_logger(logger, stream=stream, color=True, show_datetime=False)
    logger.info("colored")

    assert "\x1b[32m colored\x1b[0m" in stream.getvalue()
