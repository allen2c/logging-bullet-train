import logging

import logging_bullet_train


def test_set_logger():
    # Set up the logger
    logger = logging_bullet_train.set_logger("my_logger", level=logging.DEBUG)

    # Log messages with different severity levels
    logger.debug("This is a debug message")  # 🔎 DEBUG
    logger.info("This is an info message")  # 💡 INFO
    logger.warning("This is a warning message")  # ⭐ WARNING
    logger.error("This is an error message")  # 🚨 ERROR
    logger.critical("This is a critical message")  # 🔥 CRITICAL
    logger.log(1, "notset message")  # 🔘 UNKNOWN
