import logging

import logging_bullet_train as lbt


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
