test: clean
	python setup.py sdist
	virtualenv testenv
	pip install -E testenv/ dist/pyPostal-*tar.gz

check:
	pep8 -r --ignore=E501 pypostal
	pyflakes pypostal
	-pylint -iy --max-line-length=110 -d E1101 pypostal # -rn
	# Zeilen laenger als 110 Zeichen
	find pypostal -name '*.py' -exec awk 'length > 110' {} \;
	test 0 = `find pypostal -name '*.py' -exec awk 'length > 110' {} \; | wc -l`

upload:
	VERSION=`ls dist/ | perl -npe 's/.*-(\d+\..*?).tar.gz/$1/' | sort | tail -n 1`
	python setup.py sdist upload
	git tag v$VERSION
	git push origin --tags
	git commit -m "v$VERSION published on PyPi" -a
	git push origin

clean:
	rm -Rf testenv build dist
