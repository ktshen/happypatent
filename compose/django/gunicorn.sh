#!/bin/sh
python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi -w 2 -b unix:/app/media/gunicorn.sock -k gevent --chdir=/app --access-logfile -
