from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from settings.common_class import LoginRequiredNoRedirect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from . import serializer
from . import models
from inventario.models import Insumo
from settings.auxs_fn import ErrorToString

class CustomModelViewSet(LoginRequiredNoRedirect, viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'put', 'delete']
    permission_classes = [IsAdminUser]

class CompraCommonLogic:
    def detalle_pedido_logic(quantity):
        ## check positive value
        if quantity <= 0: raise Exception('Negative or zero: invalid quantity')

from django.core.exceptions import ObjectDoesNotExist
class PedidoInsumoCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def __table__():
        return 'pedidoinsumo'

    def __update_insumo_model__(detalles):
        for detalle_pedido in detalles:
            ## update quantities
            detalle_pedido.insumo.cantidad += detalle_pedido.cantidad
            detalle_pedido.insumo.save()

    def __update_insumo__(detalles):
        for detalle_pedido in detalles:
            insumo = Insumo.objects.get(id=int(detalle_pedido['insumo']))
            ## update quantities
            insumo.cantidad += int(detalle_pedido['cantidad'])
            insumo.save()

    def list(self, request):
        try:
            # join
            pedido_insumo = models.PedidoInsumo.objects.all().order_by('-fechaHora')
            # serializer
            serializer_class = serializer.PedidoInsumoSerializer(pedido_insumo, many=True, read_only=True)

            return Response(serializer_class.data)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def create(self, request):
        try:

            ## check if detalles is empty
            data = request.data.copy()
            detalles_data = data.pop('detalles', [])
            if not detalles_data:
                raise Exception("Details empty")

            serializer_pedido = serializer.PedidoInsumoSerializer(data=request.data)

            ## check data types
            serializer_pedido.is_valid(raise_exception=True)
            pedido_insumo = serializer_pedido.save(created_by=request.user)

            ## check for detalles
            serializers_detalles = []
            for detalle in detalles_data:
                detalle['pedidoInsumo'] = pedido_insumo.id
                serializers_detalles.append(serializer.DetallePedidoSerializer(data=detalle))

            ### check validity, logic and save
            detalle_pedido_models = []
            for serializer_detalle in serializers_detalles:
                serializer_detalle.is_valid(raise_exception=True)
                CompraCommonLogic.detalle_pedido_logic(serializer_detalle.validated_data.get('cantidad'))
                detalle_pedido_models.append(serializer_detalle.save())

            ## check if PedidoInsumo was received
            if pedido_insumo.recibido == 'Si':
                PedidoInsumoCRUD.__update_insumo_model__(detalle_pedido_models)

            return Response(serializer_pedido.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            pedido_insumo = models.PedidoInsumo.objects.get(id=pk)
            serializer_class = serializer.PedidoInsumoSerializer(pedido_insumo)

            # reverse relation (get DetallePedido)
            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def retrieve_detalles(self, request, pk):
        try:
            pedido_insumo = models.PedidoInsumo.objects.get(id=pk)
            # reverse relation (get DetallePedido)
            detalles_pedido = pedido_insumo.detalles_pedido.all()
            serializer_class = serializer.DetallePedidoSerializer(detalles_pedido, many=True, read_only=True)

            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def retrieve_presupuestos(self, request, pk):
        try:
            pedido_insumo = models.PedidoInsumo.objects.get(id=pk)
            # reverse relation (get Presupuestos)
            presupuestos = pedido_insumo.presupuestos.all()
            serializer_class = serializer.PresupuestoSerializer(presupuestos, many=True, read_only=True)

            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, pk):
        try:
            pedido_insumo = models.PedidoInsumo.objects.get(id=pk)
            if pedido_insumo.recibido == models.StatusScale.SI:
                raise Exception('PedidoInsumo ya recibido, no se pueden efectuar cambios')

            serializer_pedido = serializer.PedidoInsumoSerializer(pedido_insumo, data=request.data)
            serializer_pedido.is_valid(raise_exception=True)
            serializer_pedido.save()

            if serializer_pedido.validated_data.get('recibido') == models.StatusScale.SI:
                serializer_detalles = serializer.DetallePedidoSerializer(
                                                    models.DetallePedido.objects.filter(pedidoInsumo=pk).all(),
                                                    many=True)
                PedidoInsumoCRUD.__update_insumo_model__(models.DetallePedido.objects.filter(pedidoInsumo=pk).all())

            return Response(serializer_pedido.data)

        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            pedido_insumo = models.PedidoInsumo.objects.get(id=pk)

            if pedido_insumo.recibido == models.StatusScale.SI:
                return Response({"error": "No se puede eliminar un pedido ya recibido"}, status=status.HTTP_400_BAD_REQUEST)
            for detalles in models.DetallePedido.objects.filter(pedidoInsumo=pedido_insumo).all():
                detalles.delete()

            pedido_insumo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response({"error": "No se puede eliminar porque existe una dependencia con otro elemento"}, status=status.HTTP_409_CONFLICT)
        except Exception as e: 
            return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)

    
class PresupuestoCRUD(CustomModelViewSet):
    serializer_class = serializer.PresupuestoSerializer
    queryset = models.Presupuesto.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save(created_by=request.user)

            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def __table__():
        return 'presupuesto'

class DetallePedidoCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def __table__():
        return 'detallepedido'

    def list(self, request):
        # join
        detalle_pedido = models.DetallePedido.objects.all()
        # serializer
        serializer_class = serializer.DetallePedidoFkReplacedSerializer(detalle_pedido, many=True)
        return Response(serializer_class.data)

    def create(self, request):
        try:
            serializer_class = serializer.DetallePedidoSerializer(data=request.data)

            ## check data types
            serializer_class.is_valid(raise_exception=True)

            ## check logic
            CompraCommonLogic.detalle_pedido_logic(serializer_class.validated_data.get('cantidad'))

            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            detalle_pedido = models.DetallePedido.objects.get(id=pk)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_class = serializer.DetallePedidoFkReplacedSerializer(detalle_pedido)
        return Response(serializer_class.data)

    def update(self, request, pk):
        try:
            detalle_pedido = models.DetallePedido.objects.get(id=pk)
            serializer_class = serializer.DetallePedidoSerializer(detalle_pedido, data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data)

        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        return Response({"error": "La eliminación no está permitida"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
