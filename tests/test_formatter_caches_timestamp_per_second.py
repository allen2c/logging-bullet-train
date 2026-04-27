import logging

import logging_bullet_train as lbt


def test_formatter_caches_timestamp_per_second():
    formatter = lbt.BulletTrainFormatter(color=False, timezone="UTC")
    first = logging.LogRecord(
        "tests.time",
        logging.INFO,
        __file__,
        1,
        "first",
        (),
        None,
    )
    second = logging.LogRecord(
        "tests.time",
        logging.INFO,
        __file__,
        1,
        "second",
        (),
        None,
    )
    first.created = 1.1
    second.created = 1.9

    assert formatter.formatTime(first) == formatter.formatTime(second)
