.PHONY: hello test lint format

hello:
	python scripts/hello_llm.py

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .
