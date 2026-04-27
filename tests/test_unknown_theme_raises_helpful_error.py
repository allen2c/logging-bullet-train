import pytest

import logging_bullet_train as lbt


def test_unknown_theme_raises_helpful_error():
    with pytest.raises(ValueError, match="unknown theme"):
        lbt.get_theme("missing")
