.PHONY: install-all-requirements
install-all-requirements:
	@uv sync --all-groups --quiet

.PHONY: test
test: install-all-requirements
	@uv run pytest -n auto

.PHONY: coverage
coverage: install-all-requirements
	@./scripts/coverage.sh

.PHONY: clean
clean:
	@rm -rf .coverage htmlcov

.PHONY: lint
lint: install-all-requirements
	@uv run ruff check .
	@uv run ruff format --check .

.PHONY: lint-dotenv
lint-dotenv: install-all-requirements
	@uv run dotenv-linter .env .env.template

.PHONY: type-check
type-check: install-all-requirements
	@uv run mypy .

.PHONY: full-check
full-check: lint lint-dotenv type-check

.PHONY: fmt
fmt: install-all-requirements
	@uv run ruff format .
	@uv run ruff check --fix .

.PHONY: migrations
migrations: install-all-requirements
	@uv run ./scripts/make_migrations.py

.PHONY: migrate
migrate: install-all-requirements
	@uv run --no-dev alembic upgrade head

.PHONY: seed
seed: migrate
	@echo "Database will be flushed first. Are you sure? (y/n)"
	@read confirm && [ "$$confirm" = "y" ]
	@uv run ./scripts/seed.py

.PHONY: flush
flush: migrate
	@echo "Database will be flushed. Are you sure? (y/n)"
	@read confirm && [ "$$confirm" = "y" ]
	@uv run ./scripts/seed.py --clear

.PHONY: runserver
runserver: migrate
	@uv run main.py

.PHONY: dependency-graph
dependency-graph:
	@uv run tach sync
	@uv run tach show --web