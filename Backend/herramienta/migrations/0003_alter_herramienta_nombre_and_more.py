# Generated by Django 4.2.2 on 2023-09-05 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herramienta', '0002_estadoherramienta_userauth_herramienta_userauth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='herramienta',
            name='nombre',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='tipoherramienta',
            name='nombre',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]