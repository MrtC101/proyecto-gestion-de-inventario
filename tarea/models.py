from django.db import models

# Create your models here.

class Empleado(models.Model):
    idEmpleado = models.AutoField(primary_key=True)
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    mail = models.EmailField()
    
class EncuestaDeSatisfaccion(models.Model):
    idEncuestaDeSatisfaccion =  models.AutoField(primary_key=True)
    class EscalaSatisfaccion(models.TextChoices):
        EXELENTE = "EXT"
        BUENO = "BNO"
        DEFICIENTE = "DFI"
        MALO = "MLO"
        INDEFINIDO = "IND"
    class TiempoRespuesta(models.TextChoices):
        EXELENTE = "EXT"
        BUENO = "BNO"
        DEFICIENTE = "DFI"
        MALO = "MLO"
        INDEFINIDO = "IND"
    idOrdenDeServicio = models.ForeignKey("tarea.OrdenDeServicio", on_delete=models.DO_NOTHING)
    satisfaccion = models.CharField(
        max_length=3,
        choices=EscalaSatisfaccion.choices,
        default=EscalaSatisfaccion.INDEFINIDO
    )
    tiempoDeRespuesta = models.CharField(
        max_length=3,
        choices=TiempoRespuesta.choices,
        default=TiempoRespuesta.INDEFINIDO
    )
    Observaciones = models.CharField(max_length=255)

class OrdenDeServicio(models.Model):
    idOrdenDeServicio = models.AutoField(primary_key=True)
    class caraterScale(models.TextChoices):
        URGENTE = "URG"
        NORMAL = "NOR"
    class CateroriaScale(models.TextChoices):
        INDEFINIDO = "IND"
        
    idUsuario = models.ForeignKey("usuario.Usuario", verbose_name=("Id del usuario"), on_delete=models.DO_NOTHING)
    idTarea = models.ForeignKey("tarea.Tarea", verbose_name=(""), on_delete=models.DO_NOTHING)
    fechaDeGeneracion = models.DateField(auto_now=False, auto_now_add=False)
    caracter = models.CharField(
        max_length=3,
        choices=caraterScale.choices,
        default=caraterScale.NORMAL
    )
    categoria = models.CharField(
        max_length=3,
        choices=CateroriaScale.choices,
        default=CateroriaScale.INDEFINIDO
    )

class Tarea(models.Model):
    idTarea = models.AutoField(primary_key=True)
    idEmpleado = models.ManyToManyField("tarea.Empleado",blank=False)
    idSupTarea = models.OneToOneField("tarea.Tarea", verbose_name=("Tarea padre"), on_delete=models.DO_NOTHING,blank=False)
    legajo = models.IntegerField(unique=True)
    class TipoTarea(models.TextChoices):
        INDEFINIDO = "IND"
    tipo = models.CharField(
        max_length=3,
        choices=TipoTarea.choices,
        default=TipoTarea.INDEFINIDO
    )
    descripcion = models.CharField(max_length=255)
    fechaTentativa = models.DateField(auto_now=False, auto_now_add=False)
    fechaInicio = models.DateField(auto_now=False, auto_now_add=False)
    fechaFin = models.DateField(auto_now=False, auto_now_add=False)
    
