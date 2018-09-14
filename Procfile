web: newrelic-admin run-program uwsgi --master --pythonpath django/mdb/ --wsgi=wsgi --buffer-size=16384  --workers=4  --enable-threads --single-interpreter --http :$PORT
appartidarias-cron-sync: python django/mdb/manage.py sync_tse_2018  --settings=settings.production
appartidarias-cron-rank: python django/mdb/manage.py ranking  --settings=settings.production
release: python django/mdb/manage.py migrate
