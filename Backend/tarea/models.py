from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Empleado(models.Model):
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    mail = models.EmailField()

    class CategoriaScale(models.TextChoices):
        CAT1 = "1"
        CAT2 = "2"
        CAT3 = "3"
        CAT4 = "4"
        CAT5 = "5"
        CAT6 = "6"
        CAT7 = "7"
        CONTRATADO = "CONTRATADO"
    
    categoria = models.CharField(max_length=15,
                                 choices=CategoriaScale.choices,
                                 default=CategoriaScale.CAT1)

class OrdenServicio(models.Model):

    class CaracterScale(models.TextChoices):
        URGENTE = "URGENTE"
        NORMAL = "NORMAL"
    class CategoriaScale(models.TextChoices):
        INDEFINIDO = "INDEFINIDO"
    class StatusScale(models.TextChoices):
        EN_ESPERA = "EN_ESPERA"
        FINALIZADA = "FINALIZADA"
        EN_PROGRESO = "EN_PROGRESO"
    class EdificioScale(models.TextChoices):
        INDEFINIDO = "INDEFINIDO"
        AULAS = "AULAS"
        GOBIERNO = "GOBIERNO"
        DETI_I = "DETI-I"
        DETI_II = "DETI-II"

    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey("usuario.Usuario", verbose_name=("Id del usuario"), on_delete=models.DO_NOTHING)
    tarea = models.ForeignKey("tarea.Tarea", verbose_name=(""), on_delete=models.DO_NOTHING, null=True)
    fechaGeneracion = models.DateField(auto_now={True}, auto_now_add=False)
    sector = models.CharField(max_length=255, null=True)
    descripcion = models.CharField(max_length=255, null=True)
    fechaNecesidad = models.DateField(auto_now=False, auto_now_add=False, null=True)
    comentario = models.CharField(max_length=255, null=True)

    prioridad = models.CharField(
        max_length=15,
        choices=CaracterScale.choices,
        default=CaracterScale.NORMAL
    )
    categoria = models.CharField(
        max_length=15,
        choices=CategoriaScale.choices,
        default=CategoriaScale.INDEFINIDO
    )
    estado = models.CharField(
        max_length = 15,
        choices= StatusScale.choices,
        default= StatusScale.EN_ESPERA
    )

    edificio = models.CharField(
        max_length = 15,
        choices = EdificioScale.choices,
        default = EdificioScale.INDEFINIDO
    )
    
class EncuestaSatisfaccion(models.Model):
    class SatisfactionScale(models.TextChoices):
        EXCELENTE = "Excelente"
        BUENO = "Bueno"
        DEFICIENTE = "Deficiente"
        MALO = "Malo"
        INDEFINIDO = "Indefinido"
    class ResponseTimeScale(models.TextChoices):
        EXCELENTE = "Excelente"
        BUENO = "Bueno"
        DEFICIENTE = "Deficiente"
        MALO = "Malo"
        INDEFINIDO = "Indefinido"

    ordenServicio = models.ForeignKey(OrdenServicio, on_delete=models.DO_NOTHING)
    satisfaccion = models.CharField(
        max_length=15,
        choices=SatisfactionScale.choices,
        default=SatisfactionScale.INDEFINIDO
    )
    tiempoRespuesta = models.CharField(
        max_length=15,
        choices=ResponseTimeScale.choices,
        default=ResponseTimeScale.INDEFINIDO
    )
    observaciones = models.CharField(max_length=255, null=True)

class Tarea(models.Model):

    class TypeScale(models.TextChoices):
        REPARACION = "Reparación"
        INDEFINIDO = "Indefinido"

    id = models.AutoField(primary_key=True)
    empleado = models.ManyToManyField(Empleado, through='Tiempo', blank=False)
    #legajo = models.IntegerField(unique=True)
    tipo = models.CharField(
        max_length=15,
        choices=TypeScale.choices,
        default=TypeScale.INDEFINIDO
    )
    descripcion = models.CharField(max_length=255, null=True)
    fechaTentativa = models.DateField(auto_now=False, auto_now_add=False)
    fechaInicio = models.DateField(auto_now=False, auto_now_add=False, null=True)
    fechaFin = models.DateField(auto_now=False, auto_now_add=False, null=True)
    herramienta = models.ManyToManyField("herramienta.Herramienta")
    userAuth = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

class Tiempo(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.DO_NOTHING)
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING)
    horasEstimadas = models.IntegerField()
    horasTotales = models.IntegerField()
