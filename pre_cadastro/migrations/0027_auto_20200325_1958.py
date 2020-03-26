# Generated by Django 3.0.3 on 2020-03-25 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pre_cadastro', '0026_tipoveiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmissaoRg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.IntegerField()),
                ('titulo', models.CharField(max_length=70)),
            ],
        ),
        migrations.AddField(
            model_name='candidato',
            name='emissao_rg',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pre_cadastro.EmissaoRg'),
        ),
    ]
