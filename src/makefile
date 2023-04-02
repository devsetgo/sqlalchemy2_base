# Variables
PYTHON = python
PIP = $(PYTHON) -m pip
PYTEST = $(PYTHON) -m pytest

# Create a virtual environment
venv-create:
	python3 -m venv _venv
# && \
#     . _venv/bin/activate && \
#     pip install --upgrade pip && \
#     pip install -r src/requirements.txt

# Install dependencies
install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

# Install development dependencies
install-dev:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements/dev.txt

# Run the application with Uvicorn
run-dev:
	uvicorn service.main:app --reload --port 5000


# Run the application with Gunicorn
run-gunicorn:
	gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Migrate the database with Alembic
migrate:
	$(PYTHON) alembic upgrade head

# Run Pytest
test:
	$(PYTEST) tests/

format:
	black src/

# Clean up pycache and compiled Python files
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .mypy_cache

.PHONY: format venv-create install install-dev run-dev run-gunicorn migrate test clean
