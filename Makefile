PY_SRCS=src

.PHONY: lint fmt type check test

lint:
		uv run ruff check $(PY_SRCS) --fix

fmt:
		uv run ruff format $(PY_SRCS)

type:
		uv run mypy $(PY_SRCS)

check: lint fmt type

test:
		docker compose up -d --build --wait
		docker compose exec -T web python -m pytest -v
