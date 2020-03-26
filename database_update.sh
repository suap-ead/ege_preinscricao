#!/bin/sh
python manage.py makemigrations
python manage.py migrate
sh ./scripts/fixtures.sh