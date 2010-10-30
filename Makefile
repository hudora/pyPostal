test: clean
	python setup.py sdist
	virtualenv testenv
	pip install -E testenv/ dist/pyPostal-*tar.gz

upload:
	VERSION=`ls dist/ | perl -npe 's/.*-(\d+\..*?).tar.gz/$1/' | sort | tail -n 1`
	python setup.py sdist upload
	git tag v$VERSION
	git push origin --tags
	git commit -m "v$VERSION published on PyPi" -a
	git push origin

clean:
	rm -Rf testenv build dist
