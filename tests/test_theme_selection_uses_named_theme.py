import logging_bullet_train as lbt
from tests._helpers import stream_logger


def test_theme_selection_uses_named_theme():
    stream, logger = stream_logger("tests.theme")

    lbt.set_logger(logger, stream=stream, color=False, theme="terminal")
    logger.error("failed")

    assert "!! ERROR" in stream.getvalue()
