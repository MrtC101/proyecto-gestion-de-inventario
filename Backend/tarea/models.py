from datetime import date
from django.core.validators import MinValueValidator
from django.db import models
from settings.common_class import CommonModel
from usuario.models import Usuario

class Empleado(CommonModel):
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
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)

class Sector(models.Model):
    class EdificioScale(models.TextChoices):
        AULAS = 'AULAS'
        DETI_I = 'DETI I'
        DETI_II = 'DETI II'
        GOBIERNO = 'GOBIERNO'
        ARQUITECTURA = 'ARQUITECTURA'

    id = models.AutoField(primary_key=True)
    edificio = models.CharField(
        max_length = 12,
        choices= EdificioScale.choices
    )
    nombre = models.CharField(max_length=30)

    class Meta:
        unique_together = ('edificio', 'nombre')

class OrdenServicio(CommonModel):

    class CaracterScale(models.TextChoices):
        CRITICO = "CRITICO"
        URGENTE = "URGENTE"
        NORMAL = "NORMAL"
    class CategoriaScale(models.TextChoices):
        MODIFICACION = "MODIF/ADEC"
        FABRICACION = "FABRICACION"
        TRASLADOS = "TRASLADOS"
    class StatusScale(models.TextChoices):
        #EN_ESPERA->APROBADO->EN_PROGRESO->FINALIZADA
        #   └->REACHAZADA
        # Cuando se acepta pasa a probada, cuando se crea la tarea pasa a en progreso y cuando se termina a finalizada.
        EN_ESPERA = "EN_ESPERA"
        FINALIZADA = "FINALIZADA"
        EN_PROGRESO = "EN_PROGRESO"
        RECHAZADA = "RECHAZADA"
        APROBADA = "APROBADA"

    id = models.AutoField(primary_key=True)
    # cuando se quite null=True, modificar required=True en OrdenServicioUsuarioSerializer
    usuario = models.ForeignKey("usuario.Usuario", verbose_name=("Id del usuario"), on_delete=models.DO_NOTHING, blank=True)
    fechaGeneracion = models.DateField(auto_now=True)
    descripcion = models.CharField(max_length=255, null=True)
    fechaNecesidad = models.DateField(
            validators=[MinValueValidator(limit_value=date.today())],
            help_text='Fecha debe ser igual o posterior a la actual'
    )
    comentario = models.CharField(max_length=255, null=True)

    prioridad = models.CharField(
        max_length=15,
        choices=CaracterScale.choices,
        default=CaracterScale.NORMAL
    )
    categoria = models.CharField(
        max_length=15,
        choices=CategoriaScale.choices,
        default=CategoriaScale.MODIFICACION
    )
    estado = models.CharField(
        max_length = 15,
        choices= StatusScale.choices,
        default= StatusScale.EN_ESPERA
    )
    sector = models.ForeignKey(Sector, on_delete=models.DO_NOTHING)

    def clean(self, nuevo_estado):

        # status progression
        if self.estado == self.StatusScale.FINALIZADA:
            if nuevo_estado != self.StatusScale.FINALIZADA:
                raise Exception('Orden de servicio finalizada, no se puede cambiar el estado')
        elif self.estado == self.StatusScale.EN_PROGRESO:
            if nuevo_estado in [self.StatusScale.EN_ESPERA, 
                                self.StatusScale.APROBADA, 
                                self.StatusScale.RECHAZADA]:
                raise Exception('Orden de servicio en progreso, solo puede finalizarse')
        elif self.estado == self.StatusScale.RECHAZADA:
            if nuevo_estado in [self.StatusScale.EN_PROGRESO, 
                                self.StatusScale.FINALIZADA]: 
                raise Exception('Orden de servicio en rechazada, debe aprobarse si se desea asignar a tarea')
        elif self.estado == self.StatusScale.APROBADA:
            if nuevo_estado == self.StatusScale.FINALIZADA: 
                raise Exception('Orden de servicio aprobada, debe realizarse antes de finalizarla')
        elif self.estado == self.StatusScale.EN_ESPERA:
            if nuevo_estado in [self.StatusScale.EN_PROGRESO, 
                                self.StatusScale.FINALIZADA]: 
                raise Exception('Orden de servicio en espera, debe aprobarse o rechazarse')

    def is_rechazed(self, raise_exception=True):
        if self.estado == self.StatusScale.RECHAZADA:
            if raise_exception:
                raise Exception('La orden de servicio fue rechazada')
            return True
        return False
    
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

class Tarea(CommonModel):

    class TypeScale(models.TextChoices):
        PREVENTIVO = "Preventivo"
        CORRECTIVO = "Correctivo"
        MEJORA = "Mejora"
        PRODUCCION = "Produccion"

    class ClassificationScale(models.TextChoices):
        SANITARIOS = "Sanitarios"
        ELECTRICIDAD = "Electricidad"
        ALBAÑILERIA = "Albañileria"
        CARPINTERIA = "Carpinteria"
        REFRIGERACION = "Refrig/Calefacc"
        GAS = "Gas"
        MECANICA = "Mecanica"
        SYM = "S&M"
        PINTURA = "Pintura"
        JARDINERIA = "Jardineria"
        METALURGIA = "Metalurgia"
        AGUA = "Agua/Cloacas"
        OTROS = "Otros"


    id = models.AutoField(primary_key=True)
    empleados = models.ManyToManyField(Empleado, through='Tiempo', blank=True)
    #legajo = models.IntegerField(unique=True)
    ordenServicio = models.ForeignKey(OrdenServicio, on_delete=models.DO_NOTHING)
    tipo = models.CharField(
        max_length=15,
        choices=TypeScale.choices,
    )
    descripcion = models.CharField(max_length=255, null=True)
    
    fechaTentativa = models.DateField(
            validators=[MinValueValidator(limit_value=date.today())],
            help_text='Fecha debe ser igual o posterior a la actual'
    )
    
    fechaInicio = models.DateField(
            validators=[MinValueValidator(limit_value=date.today(),
                                          message='Fecha debe ser igual o posterior a la actual')],
            null=True
    )
    fechaFin = models.DateField(
            validators=[MinValueValidator(limit_value=date.today(),
                                          message='Fecha debe ser igual o posterior a la actual')],
            null=True
    )
    herramientas = models.ManyToManyField("herramienta.Herramienta", blank=True)
    clasificacion = models.CharField(
            max_length=15,
            choices=ClassificationScale.choices
    )
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)

class Tiempo(models.Model):

    class CategoryScale(models.TextChoices):
        SI = "Si"
        NO = "No"

    tarea = models.ForeignKey(Tarea, on_delete=models.DO_NOTHING)
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING)
    horasEstimadas = models.IntegerField(
            validators=[MinValueValidator(0,
                        message='El valor no puede ser menor a cero')],
            null=True
    )
    horasTotales = models.IntegerField(
            validators=[MinValueValidator(0,
                        message='El valor no puede ser menor a cero')],
            null=True
    )
    responsable = models.CharField(
            max_length=2,
            choices=CategoryScale.choices,
            default=CategoryScale.NO
    )
    created_by = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True)
