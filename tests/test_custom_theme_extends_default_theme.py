import logging

import logging_bullet_train as lbt
from tests._helpers import stream_logger


def test_custom_theme_extends_default_theme():
    stream, logger = stream_logger("tests.custom_theme")

    lbt.set_logger(logger, stream=stream, color=False, theme={logging.INFO: "ok"})
    logger.info("custom")
    logger.error("fallback")

    output = stream.getvalue()
    assert "ok INFO" in output
    assert "🚨 ERROR" in output
