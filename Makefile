.PHONY: hello test lint format api

hello:
	python scripts/hello_llm.py

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .

api:
	uvicorn copilot.api:app --app-dir src --reload
