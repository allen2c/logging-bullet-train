import logging_bullet_train as lbt
from tests._helpers import stream_logger


def test_format_sections_are_configurable():
    stream, logger = stream_logger("tests.sections")

    lbt.set_logger(
        logger,
        stream=stream,
        color=False,
        show_datetime=False,
        show_logger_name=False,
        show_lineno=False,
    )
    logger.info("compact")

    output = stream.getvalue()
    assert "💡 INFO" in output
    assert "tests.sections" not in output
    assert "compact" in output
