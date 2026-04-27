import logging

import pytest

import logging_bullet_train as lbt


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("info", logging.INFO),
        (logging.ERROR + 1, logging.ERROR),
        (0, lbt.LOGGING_UNKNOWN),
    ],
)
def test_to_level_accepts_names_and_ranges(value, expected):
    assert lbt.to_level(value) == expected
