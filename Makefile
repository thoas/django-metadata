pep8:
	flake8 metadata --ignore=E501,E127,E128,E124

test:
	coverage run --branch --source=metadata manage.py test metadata
	coverage report --omit=metadata/test*

release:
	python setup.py sdist register upload -s
