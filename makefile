.PHONY: build
build:
	python ./setup.py sdist bdist_wheel

.PHONY: upload_test
upload_test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload:
	twine upload dist/*

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

.PHONY: update_minor_version
update_minor_version:
	punch --part minor

.PHONY: update_patch_version
update_patch_version:
	punch --part patch

.PHONY: update_major_version
update_major_version:
	punch --part major