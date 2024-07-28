default:

install:
	deactivate; unset PIP_REQUIRE_VIRTUALENV && pip install .

editable:
	deactivate; unset PIP_REQUIRE_VIRTUALENV && pip install -e .

readme:
	./update_readme.py

clean:
	-find . -type d -name __pycache__ -exec rm -rf {} +
	-find src -type d -name "*.egg-info" -exec rm -rf {} +

.PHONY: default install editable readme test clean
