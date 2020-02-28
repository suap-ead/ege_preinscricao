#!/bin/sh
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
python manage.py loaddata ./pre_cadastro/fixtures/nivel_ensino.yaml
python manage.py loaddata ./pre_cadastro/fixtures/tipo_instituicao.yaml
python manage.py loaddata ./pre_cadastro/fixtures/ano_conclusao.yaml
python manage.py loaddata ./pre_cadastro/fixtures/necessidade_especial.yaml