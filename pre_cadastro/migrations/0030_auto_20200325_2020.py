# Generated by Django 3.0.3 on 2020-03-25 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pre_cadastro', '0029_auto_20200325_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.IntegerField()),
                ('titulo', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='candidato',
            name='turno',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pre_cadastro.Turno'),
        ),
    ]
