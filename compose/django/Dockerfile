FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN useradd -g 0 django


# Requirements have to be pulled and installed here, otherwise caching won't work
# wait for django-user_agents v0.3.1 to release
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/django/gunicorn.sh ./compose/django/entrypoint.sh /
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh\
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

COPY . /app
# Create media uploading directory
RUN mkdir -p /app/media
RUN mkdir -p /app/static

RUN chown -R django:root /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
