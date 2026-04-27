# Installation

Install the package from PyPI:

```bash
pip install logging-bullet-train
```

## Requirements

`logging-bullet-train` supports Python `3.11` and newer.

Runtime dependencies are intentionally small:

- `colorama` for terminal colors.
- `tzdata` on platforms that need an IANA timezone database.

## Development Install

For local development, install with Poetry:

```bash
poetry install --with dev
```

Run the test suite:

```bash
poetry run pytest
```

Run the documentation site locally:

```bash
poetry run mkdocs serve
```
