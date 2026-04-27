# logging-bullet-train

A bullet-train style Python logging utility with colorful, emoji-enhanced log
messages.

Documentation: <https://allen2c.github.io/logging-bullet-train/>

## Features

- Colorful log levels and readable segment separators.
- ISO-8601 timestamps with `zoneinfo` timezone support.
- 45 built-in emoji themes plus custom theme mappings.
- Idempotent logger setup to avoid duplicate log lines.
- Configurable stream, color mode, propagation, and visible format sections.

## Installation

```bash
pip install logging-bullet-train
```

For development:

```bash
poetry install --with dev
```

## Usage

```python
import logging

import logging_bullet_train as lbt

logger = lbt.set_logger("my_logger", level=logging.DEBUG)

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")
logger.log(1, "unknown message")
```

Sample output:

```text
2026-04-27T08:08:12+00:00  🔎 DEBUG     my_logger:8  debug message
2026-04-27T08:08:12+00:00  💡 INFO      my_logger:9  info message
2026-04-27T08:08:12+00:00  ⭐ WARNING   my_logger:10  warning message
```

## Configuration

```python
import logging
import sys

from logging_bullet_train import set_logger

logger = set_logger(
    "app",
    level="INFO",
    theme="rocket",
    color="auto",
    stream=sys.stderr,
    timezone="Asia/Taipei",
    show_datetime=True,
    show_logger_name=True,
    show_lineno=True,
    propagate=False,
)
```

Logging defaults to `stderr`, which is the usual choice for logs because it keeps
program output on `stdout` clean for shell pipelines.

### Themes

Use a named theme:

```python
logger = set_logger("app", theme="terminal")
```

Built-in themes:

```python
from logging_bullet_train import level_emojis

print(sorted(level_emojis))
```

Use a custom theme mapping:

```python
import logging

logger = set_logger("app", theme={logging.INFO: "ok"})
```

Custom themes are merged with the default theme, so you only need to override
the levels you care about.

### Color

```python
set_logger("app", color=True)
set_logger("app", color=False)
set_logger("app", color="auto")
set_logger("app", color="always")
set_logger("app", color="never")
```

`"auto"` enables color only for TTY streams and respects the `NO_COLOR`
environment variable.

### Format Sections

```python
set_logger(
    "app",
    show_datetime=False,
    show_logger_name=False,
    show_lineno=False,
)
```

### Logger Attributes

```python
set_logger("app", propagate=False, disabled=False)
```

`set_logger()` also avoids adding duplicate bullet-train handlers when called
more than once for the same logger and stream. Pass `replace_handlers=True` to
replace existing bullet-train handlers.

## Manual Handler Setup

```python
import logging

from logging_bullet_train import BulletTrainFormatter

handler = logging.StreamHandler()
handler.setFormatter(BulletTrainFormatter(theme="weather", color="auto"))

logger = logging.getLogger("manual")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
```

## Documentation

The documentation site is built with MkDocs Material.

Serve it locally:

```bash
poetry run mkdocs serve
```

Build it strictly:

```bash
poetry run mkdocs build --strict
```

GitHub Actions builds and deploys GitHub Pages when `main` is pushed.

## License

MIT. See [LICENSE](LICENSE).
