app:
	cd django/mdb/ && cookiecutter https://github.com/rpedigoni/cookiecutter-django-app

test:
	coverage run --branch --source=django/mdb  django/mdb/./manage.py test django/mdb/ -v 2 --failfast --settings=settings.test
	coverage report --omit=django/mdb/*/migrations*,django/mdb/settings/*,django/mdb/urls.py,django/mdb/wsgi.py,django/mdb/manage.py,django/mdb/*/tests/*,django/mdb/__init__.py

html:
	coverage html --omit=django/mdb/*/migrations*,django/mdb/settings/*,django/mdb/urls.py,django/mdb/wsgi.py,django/mdb/manage.py,django/mdb/*/tests/*,django/mdb/__init__.py
	open htmlcov/index.html

doc:
	$(MAKE) -C docs/ html
	open docs/build/html/index.html

deploy:
	fab -f django/fabfile.py deploy

clean:
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf docs/build/
