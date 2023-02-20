FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'Movies.settings'

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

EXPOSE 8000

COPY . .
COPY ./django_run.sh /
RUN chmod +x /django_run.sh

RUN adduser --disabled-password producer
RUN chown producer /opt/app/static/
USER producer

ENTRYPOINT ["/django_run.sh"]
