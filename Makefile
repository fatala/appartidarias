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
	@find . -name "*.pyc" | xargs rm -f
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name "*.DS_Store" | xargs rm -rf
	@find . -name "*.coverage" | xargs rm -f
	@find . -name "htmlcov" | xargs rm -rf
	@find . -name "docs/build" | xargs rm -rf
	@find . -name "*~" | xargs rm -f
