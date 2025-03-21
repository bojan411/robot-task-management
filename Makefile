.PHONY: deps lint test run build app seeded-app teardown seed-db reset-db

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

seeded-app:
	docker compose up -d seed

teardown:
	docker compose down

seed-db:
	poetry run python scripts/seed_db.py

reset-db:
	poetry run python scripts/seed_db.py --reset