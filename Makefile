# Variables
DOCKER_COMPOSE_FILE=docker-compose.yml
DOCKER_COMPOSE=docker-compose -f $(DOCKER_COMPOSE_FILE)

# Commands
build: ## Builds the Docker containers for the project.
	$(DOCKER_COMPOSE) build

up: ## Starts the Docker containers in the background.
	$(DOCKER_COMPOSE) up -d

down: ## Stops the Docker containers.
	$(DOCKER_COMPOSE) down

prune: ## Prunes the Docker containers.
	docker system prune

restart: ## Restarts the Docker containers.
	$(DOCKER_COMPOSE) restart

logs: ## Follows the logs of the Docker containers.
	$(DOCKER_COMPOSE) logs -f

lint: ## Runs Black, Isort, Bandit, and Flake8 on the codebase.
	$(DOCKER_COMPOSE) run web black . && \
	$(DOCKER_COMPOSE) run web isort . && \
	$(DOCKER_COMPOSE) run web bandit -r . && \
	$(DOCKER_COMPOSE) run web flake8 .

test: ## Runs Django's test suite.
	$(DOCKER_COMPOSE) run web python manage.py test

.PHONY: build up down restart logs lint test

help: ## Display this help message
	@echo "Available targets:"
	@awk -F '##' '/^[a-z_]+:[a-z ]+##/ { print "\033[34m"$$1"\033[0m" "\n" $$2 }' Makefile

default: help