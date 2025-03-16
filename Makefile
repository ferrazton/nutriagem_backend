.PHONY: run test build lint lint-python lint-frontend setup-dev setup-hooks

BACKEND_DIR := backend

# Build the Docker image (using the backend's docker-compose file)
build:
	docker-compose -f $(BACKEND_DIR)/docker-compose.yml build

# Run the server locally using Docker (using the backend's docker-compose file)
run:
	docker-compose -f $(BACKEND_DIR)/docker-compose.yml up

# Run the tests inside the Docker container
test:
	docker-compose -f $(BACKEND_DIR)/docker-compose.yml run --rm backend pytest --cov=app --cov-report=term-missing

# Lint both Python and Frontend files
lint: lint-python lint-frontend

# Lint Python files (inside the backend folder)
lint-python:
	flake8 $(BACKEND_DIR)

# Lint Frontend JS files
lint-frontend:
	pre-commit run eslint --files frontend/**/*.{js,jsx}

# Set up the development environment (Python & pre-commit)
setup-dev:
	python -m venv venv
	. venv/bin/activate && pip install pre-commit
	pre-commit install
	pre-commit autoupdate
	@echo "Note: Node.js/npm must be installed separately for frontend linting."

# Install git hooks (from a hooks directory at the repo root)
setup-hooks:
	cp hooks/pre-push .git/hooks/pre-push
	chmod +x .git/hooks/pre-push
