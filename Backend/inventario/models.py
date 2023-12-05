from django.db import models
from django.core.validators import MinValueValidator
from settings.common_class import CommonModel
from usuario.models import Usuario
from tarea.models import Tarea

class ActionScale(models.TextChoices):
    SUMAR = 'Sumar'
    RESTAR = 'Restar'

class TipoInsumo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32, unique=True)
    descripcion = models.CharField(max_length=256, null=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        texto = "{0}"
        return texto.format(self.nombre)

class Insumo(CommonModel):

    class MeasuresScale(models.TextChoices):
        METRO = 'Metro'
        LITRO = 'Litro'
        GRAMO = 'Gramo'
        CONTABLE = 'Contable'
    
    id = models.AutoField(primary_key=True)
    tipoInsumo = models.ForeignKey(TipoInsumo, on_delete=models.DO_NOTHING)
    nombre = models.CharField(max_length=32)
    unidadMedida = models.CharField(max_length=16, choices=MeasuresScale.choices, default=MeasuresScale.CONTABLE)
    cantidad = models.IntegerField(validators=[MinValueValidator(0, message='El valor no puede ser menor a cero')])
    codigo = models.CharField(max_length=16, null=True,unique=True)
    observaciones = models.CharField(max_length=256, null=True)
    puntoReposicion = models.IntegerField(validators=[MinValueValidator(0, message='El valor no puede ser menor a cero')],
                                          null=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.tipoInsumo, self.cantidad)

    def update_quantity(self, cantidad, accion=ActionScale.SUMAR):
        quant = abs(cantidad)
        if accion == ActionScale.SUMAR:
            self.cantidad += quant
        elif accion == ActionScale.RESTAR:
            if self.cantidad - quant < 0:
                raise Exception('Cantidad excedida')
            self.cantidad -= quant
        else:
            raise Exception("Acción desconocida sobre cantidad")

class OrdenRetiro(CommonModel):
    id = models.AutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.DO_NOTHING)
    tarea = models.ForeignKey(Tarea, on_delete=models.DO_NOTHING, related_name='insumos_retirados')
    cantidad = models.IntegerField(validators=[MinValueValidator(1, message='El valor no puede ser menor a uno')])
    fechaHora = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.id, self.cantidad)

class AjusteStock(CommonModel):

    id = models.AutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    observaciones = models.CharField(max_length=256)
    fecha = models.DateTimeField(auto_now=True)
    accionCantidad = models.CharField(max_length=6, choices=ActionScale.choices)
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)
