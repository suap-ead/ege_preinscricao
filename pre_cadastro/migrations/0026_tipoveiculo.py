# Generated by Django 3.0.3 on 2020-03-25 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pre_cadastro', '0025_auto_20200325_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoVeiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.IntegerField()),
                ('titulo', models.CharField(max_length=50)),
            ],
        ),
    ]
