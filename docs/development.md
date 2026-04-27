# Development

## Setup

```bash
poetry install --with dev
```

## Tests

```bash
poetry run pytest
```

The test suite keeps one test function per test file. Parametrized tests may
cover multiple cases in one file.

## Formatting

```bash
poetry run isort logging_bullet_train tests
poetry run black logging_bullet_train tests
```

Or use the Makefile:

```bash
make format-all
```

## Documentation

Serve the docs locally:

```bash
poetry run mkdocs serve
```

Build the static site:

```bash
poetry run mkdocs build --strict
```

The GitHub Actions workflow builds and deploys the site to GitHub Pages when
`main` is pushed.

## Release Checklist

1. Update `logging_bullet_train/version.py`.
2. Update `pyproject.toml`.
3. Run tests and docs build.
4. Publish the package.
5. Create the release tag.
