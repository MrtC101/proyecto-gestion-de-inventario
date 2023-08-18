# Generated by Django 4.2.2 on 2023-08-09 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0002_remove_ordencompra_id_remove_presupuesto_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresupuestoAsociado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('aprobado', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='ordencompra',
            name='idPresupuestoOrden',
        ),
        migrations.RemoveField(
            model_name='presupuestoordencompra',
            name='idOrden',
        ),
        migrations.RemoveField(
            model_name='presupuestoordencompra',
            name='idPresupuesto',
        ),
        migrations.RenameField(
            model_name='presupuesto',
            old_name='idPresupuesto',
            new_name='id',
        ),
    ]