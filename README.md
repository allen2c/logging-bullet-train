# logging-bullet-train

A bullet-train style Python logging utility that enhances your logging output with colorful and emoji-enhanced messages for better readability and quicker debugging.

## Features

- **Colorful Log Levels**: Each log level is color-coded for immediate recognition.
- **Emoji Indicators**: Visual emojis represent different log levels, making logs more intuitive.
- **ISO Datetime Formatting**: Timestamps are formatted in ISO format for consistency.
- **Customizable**: Easily configurable to fit your project's needs.
- **Supports Multiple Environments**: Compatible with various environments and Python versions.

## Installation

You can install `logging-bullet-train` using `pip`:

```bash
pip install logging-bullet-train
```

For development purposes, use Poetry to install all dependencies:

```bash
poetry install
```

## Usage

Here's a simple example to get you started:

```python
import logging

import logging_bullet_train

# Set up the logger
logger = logging_bullet_train.set_logger("my_logger", level=logging.INFO)

# Log messages with different severity levels
logger.debug("This is a debug message")  # 🫐 DEBUG
logger.info("This is an info message")  # 🍏 INFO
logger.warning("This is a warning message")  # 🍋 WARNING
logger.error("This is an error message")  # 🍒 ERROR
logger.critical("This is a critical message")  # 🌶️ CRITICAL
#  2024-12-21T08:08:12+00:00  🍏 INFO      my_logger  This is an info message
#  2024-12-21T08:08:12+00:00  🍋 WARNING   my_logger  This is a warning message
#  2024-12-21T08:08:12+00:00  🍒 ERROR     my_logger  This is an error message
#  2024-12-21T08:08:12+00:00  🌶️ CRITICAL  my_logger  This is a critical message
```

### Advanced Configuration

You can customize the logger further by modifying the `set_logger` function parameters or by extending the `ColoredIsoDatetimeFormatter`.

```python
import logging

import logging_bullet_train

# Custom logger with DEBUG level
custom_logger = logging_bullet_train.set_logger("custom_logger", level=logging.DEBUG)

custom_logger.debug("Custom debug message")
custom_logger.info("Custom info message")

```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
