#! /bin/bash

cd /app/

pip install -r requirements.txt

echo Running Migrations
python manage.py makemigrations
python manage.py migrate --noinput

echo Running server on port 8000
python manage.py runserver 0.0.0.0:8000
