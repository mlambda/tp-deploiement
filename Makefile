check:
	black --check landscapred
	mypy landscapred
	flake8 --count landscapred
	pylint landscapred
