install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

run:
	uvicorn event_platform.api:app --reload

benchmark:
	python benchmarks/throughput_benchmark.py

docker:
	docker compose up --build
