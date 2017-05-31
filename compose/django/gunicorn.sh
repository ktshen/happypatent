#!/bin/sh
python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi -w 4 -b unix:/app/media/gunicorn.sock --chdir=/app --access-logfile -
