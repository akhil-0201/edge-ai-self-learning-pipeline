.PHONY: install test lint format clean cycle status

install:
	pip install -e .[dev]

test:
	pytest tests/ -v --cov=edge_learner --cov-report=term-missing

lint:
	ruff check edge_learner/ tests/

format:
	black edge_learner/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name '*.pyc' -delete

status:
	python -m edge_learner.orchestrator.health_monitor --once

cycle:
	python -m edge_learner.orchestrator.pipeline_runner --mode maintenance

rollback:
	python -m edge_learner.deployer.rollback --force
