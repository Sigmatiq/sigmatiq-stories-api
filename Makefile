# Sigma Stories — placeholder Makefile

.PHONY: help test build lint db-migrate db-migrate-dry

help:
	@echo "Sigma Stories (placeholder product). Add real targets as it evolves."
	@echo "Targets:"
	@echo "  test   - run pytest (placeholder)"
	@echo "  build  - build wheel (placeholder)"
	@echo "  lint   - lint/type-check (placeholder)"
	@echo "  db-migrate     - apply SQL migrations in products/sigma-stories/api/migrations"
	@echo "  db-migrate-dry - list migrations without applying"

test:
	@echo "[placeholder] run: pytest -q"

build:
	@echo "[placeholder] run: python -m build"

lint:
	@echo "[placeholder] run: ruff check . && black --check . && mypy ."

# --- DB Migrations (Sigma Stories) ---
MIGRATIONS_DIR ?= api/migrations

db-migrate:
	@echo "Applying migrations in $(MIGRATIONS_DIR) using products/sigma-stories/.env"
	PYTHONPATH=. python3 scripts/apply_migrations.py --dir $(MIGRATIONS_DIR)

db-migrate-dry:
	PYTHONPATH=. python3 scripts/apply_migrations.py --dir $(MIGRATIONS_DIR) --dry-run
