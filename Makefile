.PHONY: default
default:

PHONY: install
install:
	unset PIP_REQUIRE_VIRTUALENV && pip install .

PHONY: editable
editable:
	unset PIP_REQUIRE_VIRTUALENV && pip install -e .

.PHONY: readme
readme:
	./update_readme.py

.PHONY: clean
clean:
	-find . -maxdepth 1 -type d -name __pycache__ -exec rm -rf {} +
	-find src -type d -name __pycache__ -o -name "*.egg-info" \
		-exec rm -rf {} +
