.PHONY: run tests build lint lint-python lint-frontend setup-dev setup-hooks

# Build the Docker image
build:
	docker-compose build

# Run the server locally using Docker
run:
	docker-compose up

# Run the tests inside the Docker container
tests:
	docker-compose run --rm backend pytest --cov=app --cov-report=term-missing

# Lint Python and Frontend
lint: lint-python lint-frontend

# Lint Python only
lint-python:
	flake8 .

# Lint Frontend JS/TS only
lint-frontend:
	pre-commit run eslint --files frontend/**/*.{js,jsx,ts,tsx}

# Set up development environment
setup-dev:
	python -m venv venv
	. venv/bin/activate && pip install pre-commit
	pre-commit install
	pre-commit autoupdate
	@echo "Node.js/npm must be installed separately for frontend linting"

# Install git hooks
setup-hooks:
	cp hooks/pre-push .git/hooks/pre-push
	chmod +x .git/hooks/pre-push
