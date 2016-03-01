.PHONY: build test

build:
	pip3 install pytest -U

test:
	py.test tests/