# Usage

The easiest way to use the library is `set_logger()`.

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

## Stream Choice

Logs default to `stderr`, which is the standard logging choice for command-line
tools and services. It keeps normal program output on `stdout`, so shell
pipelines can consume data without mixed log lines.

Use `stdout` explicitly when logs are the product output:

```python
import sys

logger = lbt.set_logger("cli", stream=sys.stdout)
```

## Manual Handler Setup

Use `BulletTrainFormatter` directly when you want to manage handlers yourself.

```python
import logging

from logging_bullet_train import BulletTrainFormatter

handler = logging.StreamHandler()
handler.setFormatter(BulletTrainFormatter(theme="weather", color="auto"))

logger = logging.getLogger("manual")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
```

## Exceptions

Exception formatting uses the normal `logging` machinery.

```python
logger = lbt.set_logger("app")

try:
    raise RuntimeError("boom")
except RuntimeError:
    logger.exception("request failed")
```
