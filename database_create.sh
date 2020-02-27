#!/bin/sh
python ./scripts/createdb.py pre_cadastro postgres postgres
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
sh ./scripts/fixtures.sh