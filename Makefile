.PHONY: test lint commit

test:
	uv run pytest -q

lint:
	uv run ruff check . && uv run ruff format --check .

commit:
	uv run pytest -q
	@if command -v pre-commit >/dev/null 2>&1; then pre-commit run --all-files; else uvx pre-commit run --all-files; fi
	git commit
