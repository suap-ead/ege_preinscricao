# Generated by Django 3.0.3 on 2020-05-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacao', '0006_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]