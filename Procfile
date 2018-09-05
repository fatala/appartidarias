web: gunicorn -b 0.0.0.0:$PORT -w 3 --pythonpath django/mdb wsgi
appartidarias-cron-sync: python django/mdb/manage.py sync_tse_2018  --settings=settings.production
appartidarias-cron-rank: python django/mdb/manage.py ranking  --settings=settings.production
release: python django/mdb/manage.py migrate
