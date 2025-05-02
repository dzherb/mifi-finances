.PHONY: install-all-requirements
install-all-requirements:
	@uv sync --all-groups --quiet

.PHONY: test
test: install-all-requirements
	@uv run pytest -n auto

.PHONY: coverage
coverage: install-all-requirements
	@./scripts/coverage.sh

.PHONY: lint
lint: install-all-requirements
	@uv run ruff check .
	@uv run ruff format --check .

.PHONY: type-check
type-check: install-all-requirements
	@uv run mypy .

.PHONY: full-check
full-check: lint type-check

.PHONY: fmt
fmt: install-all-requirements
	@uv run ruff check --fix .
	@uv run ruff format .

.PHONY: migrations
migrations: install-all-requirements
	@uv run ./scripts/make_migrations.py

.PHONY: migrate
migrate: install-all-requirements
	@uv run alembic upgrade head

.PHONY: seed
seed: install-all-requirements migrate
	@echo "Database will be flushed first. Are you sure? (y/n)"
	@read confirm && [ "$$confirm" = "y" ]
	@uv run ./scripts/seed.py

.PHONY: flush
flush: install-all-requirements migrate
	@echo "Database will be flushed. Are you sure? (y/n)"
	@read confirm && [ "$$confirm" = "y" ]
	@uv run ./scripts/seed.py --clear

.PHONY: runserver
runserver: install-all-requirements migrate
	@uv run uvicorn main:app --reload