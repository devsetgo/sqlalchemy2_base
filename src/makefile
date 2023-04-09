# Variables
PYTHON = python
PIP = $(PYTHON) -m pip
PYTEST = $(PYTHON) -m pytest

# Create a virtual environment
venv-create:
	python3 -m venv _venv

# Install dependencies
install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

# Install development dependencies
install-dev:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements/dev.txt

# Run tests via pre-commit and pytest
test:
	pre-commit run -a
	pytest

	coverage-badge -o coverage.svg -f

# Format code using black
format:
	black src/

# Migrate the database with Alembic
migrate:
	$(PYTHON) alembic upgrade head

# Run the application with Uvicorn
run-dev:
	uvicorn service.main:app --reload --port 5000

# Run the application with Gunicorn
run-prd:
	gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Clean up pycache and compiled Python files
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .mypy_cache

# Help function
help:
	@echo "Available commands:"
	@echo "  venv-create   Create a virtual environment"
	@echo "  install       Install dependencies"
	@echo "  install-dev   Install development dependencies"
	@echo "  run-dev       Run the application with Uvicorn"
	@echo "  run-gunicorn  Run the application with Gunicorn"
	@echo "  migrate       Migrate the database with Alembic"
	@echo "  test          Run Pytest"
	@echo "  format        Format the code using black"
	@echo "  clean         Clean up pycache and compiled Python files"

.PHONY: format venv-create install install-dev run-dev run-prd migrate test clean help
