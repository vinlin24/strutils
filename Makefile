.PHONY: default
default:

.PHONY: clean
clean:
	-find . -maxdepth 1 -type d -name __pycache__ -exec rm -rf {} +
	-find src -type d -name __pycache__ -exec rm -rf {} +
