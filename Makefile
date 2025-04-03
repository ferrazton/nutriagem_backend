.PHONY: run test build lint setup-dev setup-hooks clean
BACKEND_DIR := backend
FRONTEND_DIR := frontend
VENV := venv

# Build the Docker image (using the backend's docker-compose file)
build:
	docker-compose -f $(BACKEND_DIR)/docker-compose.yml build

# Run the server locally using Docker (using the backend's docker-compose file)
run:
	docker-compose -f $(BACKEND_DIR)/docker-compose.yml up

# Run the tests inside the Docker container (installing dev deps first)
test:
	docker-compose -f $(BACKEND_DIR)/docker-compose.yml run --rm backend sh -c '\
	  pip install --no-warn-script-location -r requirements-dev.txt && \
	  export COVERAGE_FILE=/tmp/.coverage && \
	  export PATH=$$HOME/.local/bin:$$PATH && \
	  pytest --cov=app --cov-report=term-missing'

# Run all linters
lint:
	flake8 $(BACKEND_DIR)
	pre-commit run --all-files

# Set up the development environment (Python & pre-commit)
setup-dev:
	@echo "Setting up backend environment..."
	@cd $(BACKEND_DIR) && \
		python3 -m venv $(VENV) && \
		. $(VENV)/bin/activate && \
		pip install --no-warn-script-location -q -r requirements-dev.txt && \
		pre-commit install && \
		pre-commit autoupdate
	@echo "\nSetting up frontend environment..."
	@cd $(FRONTEND_DIR) && \
		npm install
	@echo "\nDevelopment environment setup complete!"

# Install git hooks (from a hooks directory at the repo root)
setup-hooks:
	@cp hooks/pre-push .git/hooks/pre-push
	@chmod +x .git/hooks/pre-push
	@echo "Git hooks installed"

# Clean temporary files and containers
clean:
	docker-compose -f $(BACKEND_DIR)/docker-compose.yml down -v
	@rm -rf $(BACKEND_DIR)/$(VENV) $(BACKEND_DIR)/.coverage $(FRONTEND_DIR)/node_modules
	@find . -name '__pycache__' -exec rm -rf {} +
	@echo "Cleaned all temporary files"
