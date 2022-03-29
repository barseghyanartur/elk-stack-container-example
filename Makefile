.PHONY: help clean clean-build clean-pyc clean-test lint test dist all pip-install pip-compile create-venv migrations migrate docker-pip-compile

help:
	@echo "clean | Remove all build, test, coverage and Python artifacts"
	@echo "clean-build | Remove build artifacts"
	@echo "clean-pyc | Remove Python file artifacts"
	@echo "clean-logs | Remove logs artifacts"
	@echo "run | Run the project with Docker"
	@echo "shell | Jump into the Django shell inside the Docker container"
	@echo "bash | Jump into the bash inside the Docker container"
	@echo "ingest-logs | Run the command to ingest logs inside the Docker container"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf **/*.egg-info
	rm -rf static/CACHE

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-logs:
	rm -rf logs/*.log;

run:
	docker-compose up;

build:
	docker-compose build;

build-%:
	docker-compose build $*;

ingest-logs:
	docker-compose exec ingest-api python /usr/src/app/ingest.py;
	status=$$?; \
	exit $$status

shell:
	docker-compose exec ingest-api python /usr/src/app/main.py shell

bash:
	docker exec -it ingest-api /bin/bash

make-migrations:
	docker-compose exec ingest-api python /usr/src/app/main.py makemigrations

migrate:
	docker-compose exec ingest-api python /usr/src/app/main.py migrate

show-migrations:
	docker-compose exec ingest-api python /usr/src/app/main.py showmigrations

show-urls:
	docker-compose exec ingest-api python /usr/src/app/main.py show_urls

all: clean run ingest-logs
