# Generated by Django 4.2.2 on 2023-09-05 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_ajustestock_userauth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoinsumo',
            name='nombre',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]