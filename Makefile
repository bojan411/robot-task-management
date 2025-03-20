.PHONY: deps lint test run build app teardown seed-db reset-db

deps:
	poetry install

lint:
	ruff check

test:
	poetry run pytest

run:
	poetry run flask run

build:
	docker compose build

app:
	docker compose up -d

teardown:
	docker compose down

seed-db:
	poetry run python scripts/seed_db.py

reset-db:
	poetry run python scripts/seed_db.py --reset