.PHONY: help install install-dev lint format test test-cov audit build docker clean play

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: install ## Install dev dependencies
	pip install -r requirements-dev.txt

lint: ## Run linter, format check, and type check (matches CI)
	ruff check .
	ruff format --check .
	mypy games/ standalone/ securityquest/

format: ## Format code
	ruff format .

test: ## Run tests
	pytest tests/ -v

test-cov: ## Tests with coverage
	pytest tests/ --cov=securityquest --cov=games --cov=standalone --cov-report=term-missing --cov-fail-under=90

audit: ## Scan dependencies and source for known vulnerabilities
	pip-audit -r requirements.txt
	pip-audit -r requirements-dev.txt
	bandit -r games/ standalone/ securityquest/ -ll

build: ## Install the package itself (verifies packaging, matches CI)
	pip install .

docker: ## Build and run the Docker image
	docker build -t securityquest-academy .
	docker run --rm -it securityquest-academy

play: ## Launch the academy
	python -m securityquest

clean: ## Remove caches and packaging artifacts
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
