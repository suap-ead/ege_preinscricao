python ./scripts/createdb.py pre_cadastro postgres postgres

python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

python manage.py loaddata ./pre_cadastro/fixtures/nacionalidade.yaml
python manage.py loaddata ./pre_cadastro/fixtures/estado.yaml
python manage.py loaddata ./pre_cadastro/fixtures/estado_civil.yaml
python manage.py loaddata ./pre_cadastro/fixtures/pais_origem.yaml
python manage.py loaddata ./pre_cadastro/fixtures/raca.yaml
python manage.py loaddata ./pre_cadastro/fixtures/responsavel.yaml
python manage.py loaddata ./pre_cadastro/fixtures/sexo.yaml
python manage.py loaddata ./pre_cadastro/fixtures/tipo_sanguineo.yaml
python manage.py loaddata ./pre_cadastro/fixtures/transporte_publico.yaml
python manage.py loaddata ./pre_cadastro/fixtures/zona_residencial.yaml