from rest_framework import serializers
from . import models
from herramienta.serializer import HerramientaSerializer
from inventario.serializer import OrdenRetiroSerializer

class EmpleadoSerializer(serializers.ModelSerializer):
    """
    Retrieves all fields in Empleado
    """

    class Meta:
        model = models.Empleado
        fields = '__all__'

class EncuestaSatisfaccionSerializer(serializers.ModelSerializer):
    """
    Retrieves all fields in EncuestaSatisfaccion
    """

    class Meta:
        model = models.EncuestaSatisfaccion
        fields = '__all__'

class OrdenServicioSerializer(serializers.ModelSerializer):
    """
    Retrieves all fields in OrdenServicio
    """

    class Meta:
        model = models.OrdenServicio
        fields = '__all__'

class OrdenServicioUsuarioSerializer(serializers.ModelSerializer):
    """
    Retrieves fields from OrdenServicio
    Add fields for get:
    Usuario.apellido
    Usuario.nombre
    Usuario.id
    Sector.nombre
    Sector.subsector
    """

    usuarioApellido = serializers.CharField(source='usuario.last_name', required=False)
    usuarioNombre = serializers.CharField(source='usuario.first_name', required=False)
    usuarioID = serializers.IntegerField(source='usuario.id', required=False)
    edificio = serializers.CharField(source='sector.edificio')
    sector = serializers.CharField(source='sector.nombre')
    sectorID = serializers.IntegerField(source='sector.id')
    class Meta:
        model = models.OrdenServicio
        fields = ['id', 'fechaGeneracion', 
                  'descripcion', 'fechaNecesidad', 'comentario',
                  'prioridad', 'categoria', 'estado',
                  'usuarioNombre', 'usuarioApellido',
                  'usuarioID',
                  'edificio', 'sector','sectorID']

class TiempoSerializer(serializers.ModelSerializer):
    """
    Retrieves all fields in Tiempo
    """

    class Meta:
        model = models.Tiempo
        fields = '__all__'

class TareaSerializer(serializers.ModelSerializer):
    """
    Retrieves all fields in Tarea
    """

    class Meta:
        model = models.Tarea
        fields = '__all__'

class TareaJoinedSerializer(TareaSerializer):
    empleados = EmpleadoSerializer(many=True, required=False)
    tiempo = TiempoSerializer(many=True, required=False)
    herramientas = HerramientaSerializer(many=True, required=False)
    # Es necesario retiros_insumos acá? Se recupera en la vista TareaCRUD (retrieve y list)
    retiros_insumos = OrdenRetiroSerializer(many=True, required=False)

class SectorSubsectorSerializer(serializers.ModelSerializer):
    """
    Exclude edificio field in Sector
    """

    class Meta:
        model = models.Sector
        exclude = ['edificio']

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sector
        fields = '__all__'
