import io
import logging
import re

import pytest

import logging_bullet_train as lbt

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def test_set_logger_writes_once_without_duplicate_handlers():
    stream = io.StringIO()
    logger = logging.getLogger("tests.once")
    logger.handlers.clear()

    lbt.set_logger(logger, stream=stream, color=False, propagate=False)
    lbt.set_logger(logger, stream=stream, color=False, propagate=False)

    logger.info("hello")

    assert stream.getvalue().count("hello") == 1
    assert len(logger.handlers) == 1
    assert logger.propagate is False


def test_set_logger_can_replace_existing_bullet_train_handler():
    first_stream = io.StringIO()
    second_stream = io.StringIO()
    logger = logging.getLogger("tests.replace")
    logger.handlers.clear()

    lbt.set_logger(logger, stream=first_stream, color=False)
    lbt.set_logger(logger, stream=second_stream, color=False, replace_handlers=True)

    logger.warning("moved")

    assert first_stream.getvalue() == ""
    assert "moved" in second_stream.getvalue()
    assert len(logger.handlers) == 1


def test_theme_selection_uses_named_theme():
    stream = io.StringIO()
    logger = logging.getLogger("tests.theme")
    logger.handlers.clear()

    lbt.set_logger(logger, stream=stream, color=False, theme="terminal")
    logger.error("failed")

    assert "!! ERROR" in stream.getvalue()


def test_custom_theme_extends_default_theme():
    stream = io.StringIO()
    logger = logging.getLogger("tests.custom_theme")
    logger.handlers.clear()

    lbt.set_logger(logger, stream=stream, color=False, theme={logging.INFO: "ok"})
    logger.info("custom")
    logger.error("fallback")

    output = stream.getvalue()
    assert "ok INFO" in output
    assert "🚨 ERROR" in output


def test_color_false_removes_ansi_codes():
    stream = io.StringIO()
    logger = logging.getLogger("tests.no_color")
    logger.handlers.clear()

    lbt.set_logger(logger, stream=stream, color=False)
    logger.info("plain")

    assert not ANSI_RE.search(stream.getvalue())


def test_color_auto_respects_no_color(monkeypatch):
    stream = io.StringIO()
    stream.isatty = lambda: True  # type: ignore[attr-defined]
    logger = logging.getLogger("tests.no_color_env")
    logger.handlers.clear()
    monkeypatch.setenv("NO_COLOR", "1")

    lbt.set_logger(logger, stream=stream, color="auto")
    logger.info("plain")

    assert not ANSI_RE.search(stream.getvalue())


def test_format_sections_are_configurable():
    stream = io.StringIO()
    logger = logging.getLogger("tests.sections")
    logger.handlers.clear()

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


def test_exception_formatting_is_preserved():
    stream = io.StringIO()
    logger = logging.getLogger("tests.exception")
    logger.handlers.clear()

    lbt.set_logger(logger, stream=stream, color=False)
    try:
        raise RuntimeError("boom")
    except RuntimeError:
        logger.exception("failed")

    output = stream.getvalue()
    assert "failed" in output
    assert "Traceback" in output
    assert "RuntimeError: boom" in output


def test_resolve_timezone_uses_tz_env(monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Taipei")

    timezone = lbt.resolve_timezone()

    assert str(timezone) == "Asia/Taipei"


def test_resolve_timezone_falls_back_to_utc(monkeypatch):
    monkeypatch.setenv("TZ", "Invalid/Zone")

    timezone = lbt.resolve_timezone()

    assert str(timezone) == "UTC"


def test_all_builtin_themes_are_complete():
    required_levels = {
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
        lbt.LOGGING_UNKNOWN,
    }

    assert len(lbt.level_emojis) >= 45
    for theme in lbt.level_emojis.values():
        assert required_levels <= theme.keys()


def test_unknown_theme_raises_helpful_error():
    with pytest.raises(ValueError, match="unknown theme"):
        lbt.get_theme("missing")


def test_to_level_accepts_names_and_ranges():
    assert lbt.to_level("info") == logging.INFO
    assert lbt.to_level(logging.ERROR + 1) == logging.ERROR
    assert lbt.to_level(0) == lbt.LOGGING_UNKNOWN
