FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'Movies.settings'

RUN apt-get update

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
#     && mkdir -p /opt/app/static/ \
#     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

#RUN adduser --disabled-password producer
#USER producer

EXPOSE 8000

COPY . .

#RUN python manage.py collectstatic --clear --noinput  # && python manage.py compilemessages
#
#CMD ["python", "manage.py", "runserver"]
#CMD ["entrypoint.sh", "gunicorn", "--bind", "0.0.0.0:8000", "Movies.wsgi"]