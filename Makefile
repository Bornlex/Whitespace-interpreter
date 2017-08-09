test:
	echo '[*] testing'
	echo '[*] cleaning results directory'
	rm tests/results/* || true
	python tests.py
	echo '[*] end testing'
