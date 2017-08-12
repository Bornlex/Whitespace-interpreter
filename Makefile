test:
	@echo '[*] cleaning results directory'
	@rm tests/results/* 2> /dev/null || true
	@python tests.py
