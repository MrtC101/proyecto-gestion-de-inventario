from django.db import models
from settings.common_class import CommonModel
from usuario.models import Usuario

class StatusScale(models.TextChoices):
    DISPONIBLE = 'Disponible'
    EN_USO = 'En uso'
    EN_REPARACION = 'En reparación'
    MAL_ESTADO = 'En mal estado'
    ELIMINADA = 'Eliminada'

class TipoHerramienta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32, unique=True)
    descripcion = models.CharField(max_length=256, null=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        texto = "{0}"
        return texto.format(self.nombre)

class Herramienta(CommonModel):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32)
    tipoHerramienta = models.ForeignKey(TipoHerramienta, on_delete=models.DO_NOTHING)
    codigo = models.CharField(max_length=16, null=True,unique=True)

    fechaAlta = models.DateField(auto_now_add=True)
    observaciones = models.CharField(max_length=255, null=True)
    estado = models.CharField(max_length=15, choices=StatusScale.choices, default=StatusScale.DISPONIBLE)
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        unique_together = ('nombre', 'codigo')

    def __str__(self):
        texto = "{0} [{1}]"
        return texto.format(self.nombre, self.estado)    
    
    def is_available(self, raise_exception=True):
        if self.estado != StatusScale.DISPONIBLE:
            if raise_exception:
                raise Exception('Herramienta no disponible')
            return False
        return True


class EstadoHerramienta(CommonModel):
    herramienta = models.ForeignKey(Herramienta, on_delete=models.DO_NOTHING)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=16, choices=StatusScale.choices, default=StatusScale.DISPONIBLE)
    observaciones = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)
