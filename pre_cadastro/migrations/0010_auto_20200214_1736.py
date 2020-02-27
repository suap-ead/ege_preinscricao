# Generated by Django 3.0.3 on 2020-02-14 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pre_cadastro', '0009_auto_20200214_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZonaResidencial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.IntegerField()),
                ('titulo', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='candidato',
            name='zona_residencial',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pre_cadastro.ZonaResidencial'),
        ),
    ]