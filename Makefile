# Development
format-all:
	@poetry run isort logging_bullet_train tests
	@poetry run black logging_bullet_train tests

install-all:
	poetry install -E all --with dev

update-all:
	poetry update
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	poetry export --without-hashes -E all --with dev -f requirements.txt --output requirements-all.txt

# Docs
mkdocs:
	poetry run mkdocs serve

# Tests
pytest:
	poetry run pytest --cov=logging_bullet_train --cov-report=term-missing
