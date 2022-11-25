#!/bin/sh

echo "Waiting for db..."

echo $SQL_HOST

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "DB started"

python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000