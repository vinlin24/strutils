.PHONY: default
default:

PHONY: install
install:
	deactivate; unset PIP_REQUIRE_VIRTUALENV && pip install .

PHONY: editable
editable:
	deactivate; unset PIP_REQUIRE_VIRTUALENV && pip install -e .

.PHONY: readme
readme:
	./update_readme.py

.PHONY: test
test:
	cd test && python -m unittest

.PHONY: clean
clean:
	-find . -type d -name __pycache__ -exec rm -rf {} +
	-find src -type d -name "*.egg-info" -exec rm -rf {} +
