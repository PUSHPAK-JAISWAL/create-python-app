# Root task entrypoints (uv workspace). Tools land in Epic 2 (#17–#20).
.PHONY: sync test lint typecheck build help

help:
	@echo "Targets: sync test lint typecheck build"
	@echo "All commands run via uv from the workspace root."

sync:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run pyright

build:
	uv build --all --out-dir dist
