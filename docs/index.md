# logging-bullet-train

`logging-bullet-train` is a small Python logging utility that formats standard
library logs as colorful, segmented, bullet-train style lines.

It is designed to stay close to `logging`: you still use normal loggers,
handlers, levels, propagation, and streams. The package only adds a formatter,
a convenient `set_logger()` helper, and a curated set of emoji themes.

## Highlights

- Colorful level, logger, and message sections.
- ISO-8601 timestamps backed by `zoneinfo`.
- 45 built-in emoji themes.
- Custom emoji theme mappings.
- Idempotent logger setup to avoid duplicate log lines.
- `stderr` logging by default, with explicit stream control.
- `NO_COLOR` aware color auto-detection.
- Cached formatter hot path for low per-record overhead.

## Quick Example

```python
import logging

import logging_bullet_train as lbt

logger = lbt.set_logger("app", level=logging.DEBUG, theme="rocket")

logger.debug("debug message")
logger.info("ready")
logger.warning("check this")
logger.error("failed")
```

## Sample Output

```text
2026-04-27T08:08:12+00:00  🛠️ DEBUG     app:7  debug message
2026-04-27T08:08:12+00:00  🚄 INFO      app:8  ready
2026-04-27T08:08:12+00:00  🚦 WARNING   app:9  check this
2026-04-27T08:08:12+00:00  🛑 ERROR     app:10  failed
```

## Project Shape

The public API is intentionally compact:

- `set_logger()` for normal setup.
- `BulletTrainFormatter` for manual handler setup.
- `IsoDatetimeFormatter` for ISO timestamp formatting.
- `level_emojis` and `get_theme()` for theme discovery.
- `to_level()` for normalizing level values into styled buckets.
