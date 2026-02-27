.PHONY: format lint test build

format:
	ruff format .
	ruff check --fix .

lint:
	ruff check .

test:
	pytest

build:
	pip install build --quiet
	python -m build
