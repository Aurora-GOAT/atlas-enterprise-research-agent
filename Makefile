.PHONY: install run test
install:
	python -m pip install -r requirements-dev.txt
run:
	python run.py
test:
	pytest -q
