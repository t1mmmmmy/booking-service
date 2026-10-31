PY_SRCS=src

.PHONY: lint fmt type check

lint:
		uv run ruff check $(PY_SRCS) --fix

fmt:
		uv run ruff format $(PY_SRCS)

type:
		uv run mypy $(PY_SRCS)

check: lint fmt type