.PHONY: build
build:
	python ./setup.py sdist bdist_wheel

.PHONY: upload_test
upload_test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload:
	twine upload dist/*