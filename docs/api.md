# API

## `set_logger()`

```python
set_logger(
    logger,
    *,
    level=logging.DEBUG,
    handler_level=None,
    theme="default",
    color="auto",
    stream=None,
    timezone=None,
    show_datetime=True,
    show_level=True,
    show_logger_name=True,
    show_lineno=True,
    show_message=True,
    propagate=None,
    disabled=None,
    replace_handlers=False,
)
```

Configures and returns a standard `logging.Logger`.

`logger` may be a logger name or an existing `logging.Logger` instance.

## `BulletTrainFormatter`

Formatter that renders the bullet-train log line.

```python
from logging_bullet_train import BulletTrainFormatter
```

Constructor options mirror the formatting-related options on `set_logger()`:

- `theme`
- `color`
- `stream`
- `timezone`
- `show_datetime`
- `show_level`
- `show_logger_name`
- `show_lineno`
- `show_message`

## `IsoDatetimeFormatter`

Base formatter that provides ISO-8601 timestamp formatting with `zoneinfo`.

```python
from logging_bullet_train import IsoDatetimeFormatter
```

## Themes

```python
from logging_bullet_train import get_theme, level_emojis
```

`level_emojis` is the registry of built-in themes.

`get_theme()` accepts a theme name or custom level mapping. Custom mappings are
merged with the default theme.

## Levels

```python
from logging_bullet_train import LOGGING_UNKNOWN, to_level
```

`LOGGING_UNKNOWN` is the package's low custom level for messages below
`logging.DEBUG`.

`to_level()` normalizes string or numeric levels into the formatter's styled
level buckets.

## Version

```python
from logging_bullet_train import VERSION, __version__
```
