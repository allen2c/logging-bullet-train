# Configuration

`set_logger()` keeps configuration explicit while staying close to standard
library logging.

```python
import logging
import sys

from logging_bullet_train import set_logger

logger = set_logger(
    "app",
    level="INFO",
    handler_level=logging.DEBUG,
    theme="rocket",
    color="auto",
    stream=sys.stderr,
    timezone="Asia/Taipei",
    show_datetime=True,
    show_level=True,
    show_logger_name=True,
    show_lineno=True,
    show_message=True,
    propagate=False,
    disabled=False,
)
```

## Themes

Use one of the built-in themes:

```python
logger = set_logger("app", theme="terminal")
```

List all themes:

```python
from logging_bullet_train import level_emojis

print(sorted(level_emojis))
```

Override only the levels you care about:

```python
import logging

logger = set_logger("app", theme={logging.INFO: "ok"})
```

Custom themes are merged with the default theme.

## Color

Color accepts booleans or named modes:

```python
set_logger("app", color=True)
set_logger("app", color=False)
set_logger("app", color="auto")
set_logger("app", color="always")
set_logger("app", color="never")
```

`"auto"` enables color only for TTY streams and respects `NO_COLOR`.

## Format Sections

Each visible section can be disabled:

```python
set_logger(
    "app",
    show_datetime=False,
    show_logger_name=False,
    show_lineno=False,
)
```

## Logger Attributes

Use `propagate` and `disabled` when you want `set_logger()` to configure common
logger attributes at the same time as the handler.

```python
set_logger("app", propagate=False, disabled=False)
```

`set_logger()` is idempotent for the same logger and stream. It reuses the
existing bullet-train handler instead of adding duplicate handlers.

To replace existing bullet-train handlers:

```python
set_logger("app", replace_handlers=True)
```

## Timezones

Pass a timezone name or `datetime.tzinfo` object:

```python
set_logger("app", timezone="UTC")
set_logger("app", timezone="Asia/Taipei")
```

When no timezone is passed, the formatter checks `TZ` and falls back to `UTC`.
