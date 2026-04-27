import logging_bullet_train as lbt
from tests._helpers import ANSI_RE, TtyStringIO, stream_logger


def test_color_auto_respects_no_color(monkeypatch):
    _, logger = stream_logger("tests.no_color_env")
    stream = TtyStringIO()
    monkeypatch.setenv("NO_COLOR", "1")

    lbt.set_logger(logger, stream=stream, color="auto")
    logger.info("plain")

    assert not ANSI_RE.search(stream.getvalue())
