.PHONY: help install install-dev test test-cov lint format type-check clean build docs

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install the package with development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	python -m pytest autopost/tests/ -v

test-cov: ## Run tests with coverage
	python -m pytest autopost/tests/ --cov=autopost --cov-report=html --cov-report=term

lint: ## Run linting
	flake8 autopost/

format: ## Format code with black
	black autopost/

type-check: ## Run type checking
	mypy autopost/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	python setup.py sdist bdist_wheel

docs: ## Build documentation
	@echo "Documentation is in the docs/ directory"

run-test: ## Run a test post
	python -m autopost --test

run-post: ## Make a single post
	python -m autopost --post

run-status: ## Check bot status
	python -m autopost --status

run-bot: ## Start the bot
	python -m autopost

setup-db: ## Set up database
	mysql -u root -p < scripts/setup_database.sql

setup-service: ## Set up systemd service
	sudo bash scripts/setup_background_service.sh

start-service: ## Start the systemd service
	sudo bash scripts/manage_service.sh start

stop-service: ## Stop the systemd service
	sudo bash scripts/manage_service.sh stop

status-service: ## Check systemd service status
	sudo bash scripts/manage_service.sh status

all: format lint type-check test ## Run all quality checks 