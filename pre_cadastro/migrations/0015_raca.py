# Generated by Django 3.0.3 on 2020-02-27 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pre_cadastro', '0014_auto_20200215_0252'),
    ]

    operations = [
        migrations.CreateModel(
            name='Raca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.IntegerField()),
                ('titulo', models.CharField(max_length=50)),
            ],
        ),
    ]
