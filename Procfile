web: gunicorn -b 0.0.0.0:$PORT -w 3 --pythonpath django/mdb wsgi
cron: python django/mdb/manage.py sync_tse_2018  --settings=settings.production
release: python django/mdb/manage.py migrate
