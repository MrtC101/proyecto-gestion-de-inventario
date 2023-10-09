from rest_framework import viewsets
from . import serializer
from . import models

class CustomModelViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'put', 'delete']

class PedidoInsumoCRUD(CustomModelViewSet):
    serializer_class = serializer.PedidoInsumoSerializer
    queryset = models.PedidoInsumo.objects.all()

    def __table__():
        return 'pedidoinsumo'
    
class PresupuestoCRUD(CustomModelViewSet):
    serializer_class = serializer.PresupuestoSerializer
    queryset = models.Presupuesto.objects.all()

    def __table__():
        return 'presupuesto'

class DetallePedidoCRUD(CustomModelViewSet):
    serializer_class = serializer.DetallePedidoSerializer
    queryset = models.DetallePedido.objects.all()

    def __table__():
        return 'detallepedido'
