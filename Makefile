.PHONY: help install install-dev lint format test test-cov clean play

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: install ## Install dev dependencies
	pip install -r requirements-dev.txt

lint: ## Run linter
	ruff check securityquest/ games/ tests/

format: ## Format code
	ruff format securityquest/ games/ tests/

test: ## Run tests
	pytest tests/ -v

test-cov: ## Tests with coverage
	pytest tests/ --cov=securityquest --cov=games --cov-report=term-missing

play: ## Launch the academy
	python -m securityquest

clean: ## Remove caches
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
