# Development
format-all:
	@isort logging_bullet_train tests
	@black logging_bullet_train tests

install-all:
	poetry install -E all --with dev

update-all:
	poetry update
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	poetry export --without-hashes -E all --with dev -f requirements.txt --output requirements-all.txt

# Services
run-svc:
	fastapi run functic/app.py

run-svc-dev:
	fastapi dev functic/app.py

# Docs
mkdocs:
	mkdocs serve

# Tests
pytest:
	python -m pytest --cov=languru --cov-config=.coveragerc --cov-report=xml:coverage.xml
