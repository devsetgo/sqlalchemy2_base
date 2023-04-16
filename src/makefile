# Variables
PYTHON = python
PIP = $(PYTHON) -m pip
PYTEST = $(PYTHON) -m pytest

# Create a virtual environment
venv-create:
	python -m venv _venv

# Install dependencies
install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

# Install development dependencies
install-dev:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements/dev.txt

# Sort imports using isort
isort:
	isort service
	isort tests

# Run autoflake
autoflake:
	autoflake --in-place --remove-all-unused-imports -r service

# run flake8
flake8-report:
	./_scripts/flake8.sh
# Format code using black
format:
	black service
	black tests

# Run all formatting and cleanup
spring-clean:
	$(MAKE) isort
	$(MAKE) autoflake
	$(MAKE) format

# Run tests via pre-commit and pytest
test:
	pre-commit run -a
	pytest --cov=./ --cov-report=html --cov-report=xml -ra --tb=short -p pytester
	coverage-badge -o coverage.svg -f

# Migrate the database with Alembic
migrate:
	$(PYTHON) alembic upgrade head

# Run the application with Uvicorn
run-dev:
	uvicorn service.main:app --reload --port 5000

# Run the application with Gunicorn
run-prd:
	gunicorn service.main:app -w 4 -k uvicorn.workers.UvicornWorker

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
	@echo "  isort         Sort imports using isort"
	@echo "  autoflake     Run autoflake"
	@echo "  test          Run tests via pre-commit and pytest"
	@echo "  format        Format code using black"
	@echo "  spring-clean  Run all formatting and cleanup"
	@echo "  migrate       Migrate the database with Alembic"
	@echo "  run-dev       Run the application with Uvicorn"
	@echo "  run-prd       Run the application with Gunicorn"
	@echo "  clean         Clean up pycache and compiled Python files"
	@echo ""

.PHONY: format venv-create install install-dev run-dev run-prd migrate spring-clean test clean help autoflake

