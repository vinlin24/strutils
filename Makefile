default:

install:
	deactivate; unset PIP_REQUIRE_VIRTUALENV && pip install .

editable:
	deactivate; unset PIP_REQUIRE_VIRTUALENV && pip install -e .

readme: README.md

README.md: $(wildcard src/strutils/*.py)
	./update_readme.py

hooks:
	cp --verbose pre-commit.sh .git/hooks/pre-commit

test:
	./test.sh

clean:
	-find . -type d -name __pycache__ -exec rm -rf {} +
	-find src -type d -name "*.egg-info" -exec rm -rf {} +

.PHONY: default install editable readme hooks test clean
