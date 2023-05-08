#!/bin/bash

APP_DIR=../application/
python3 -m venv $APP_DIR/.venv
source $APP_DIR/.venv/bin/activate
pip3 install --no-cache-dir -r requirements.txt
python3 manage.py makemigrations auth django_celery_results post_office posts
python3 manage.py migrate
celery --app application worker -l INFO 2>&1 &
python3 manage.py runserver 0.0.0.0:8000