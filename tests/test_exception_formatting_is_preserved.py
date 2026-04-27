import logging_bullet_train as lbt
from tests._helpers import stream_logger


def test_exception_formatting_is_preserved():
    stream, logger = stream_logger("tests.exception")

    lbt.set_logger(logger, stream=stream, color=False)
    try:
        raise RuntimeError("boom")
    except RuntimeError:
        logger.exception("failed")

    output = stream.getvalue()
    assert "failed" in output
    assert "Traceback" in output
    assert "RuntimeError: boom" in output
