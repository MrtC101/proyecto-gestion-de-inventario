from django.db import models
from django.contrib.auth.models import User

class TipoInsumo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32, unique=True)
    descripcion = models.CharField(max_length=256, null=True)

    def __str__(self):
        texto = "{0}"
        return texto.format(self.nombre)

class Insumo(models.Model):
    id = models.AutoField(primary_key=True)
    tipoInsumo = models.ForeignKey(TipoInsumo, on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=32)
    MEDIDA_CHOICES = (
        ('metro', 'metro'),
        ('litro', 'litro'),
        ('gramo', 'gramo'),
        ('contable', 'contable'),
    )
    unidadMedida = models.CharField(max_length=16, choices=MEDIDA_CHOICES, default='contable')
    cantidad = models.IntegerField()
    codigo = models.CharField(max_length=16, null=True)
    observaciones = models.CharField(max_length=256, null=True)
    puntoReposicion = models.IntegerField(null=True)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.tipoInsumo, self.cantidad)

class OrdenRetiro(models.Model):
    id = models.AutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.DO_NOTHING)
    tarea = models.ForeignKey('tarea.Tarea', on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    fechaHora = models.DateTimeField(auto_now=True)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.id, self.cantidad)

class AjusteStock(models.Model):
    id = models.AutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    observaciones = models.CharField(max_length=256)
    fecha = models.DateTimeField(auto_now=True)
    
    ACCION_CANTIDAD = (
            ("+", "+"),
            ("-", "-"),
    )
    accionCantidad = models.CharField(max_length=1, choices=ACCION_CANTIDAD, default='+')
    userAuth = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
