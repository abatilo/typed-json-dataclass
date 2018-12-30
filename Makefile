all: test

lint:
	pipenv run python -m flake8 --show-source --import-order-style pep8

test: lint
	pipenv run python -m pytest --cov-report xml:codecov.xml --cov=typed_json_dataclass --cov-report=html --junit-xml=coverage.xml --cov-branch --cov-fail-under=95 tests/
