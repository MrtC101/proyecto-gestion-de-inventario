from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from settings.common_class import LoginRequiredNoRedirect
from rest_framework.exceptions import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializer
from . import models
from settings.auxs_fn import ErrorToString, create_hash


class CustomModelViewSet(LoginRequiredNoRedirect, viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'put', 'delete']
    permission_classes = [IsAdminUser]

class InventarioCommonLogic:
    def create_orden_retiro(data, user):
        ## check data types
        serializer_class = serializer.OrdenRetiroSerializer(data=data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save(created_by=user)

        ## update cantidad from Insumo
        insumo = models.Insumo.objects.get(id=data.get('insumo'))
        insumo.is_active_(raise_exception=True, msg='Insumo no existente')
        insumo.update_quantity(int(data['cantidad']), models.ActionScale.RESTAR)
        
        insumo.save()
        return serializer_class

class TipoInsumoCRUD(CustomModelViewSet):
    serializer_class = serializer.TipoInsumoSerializer
    queryset = models.TipoInsumo.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save(created_by=request.user)

            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            tipo_insumo = models.TipoInsumo.objects.get(id=pk)
            tipo_insumo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response({"error": "No se puede eliminar porque existe una dependencia con otro elemento"}, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Except as e: 
            return Response({"error", str(e)}, status=status.HTTP_400_NOT_FOUND)

    def __table__():
        return 'tipoinsumo'

class InsumoCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def __table__():
        return 'insumo'

    def list(self, request):
        # join
        insumo = models.Insumo.objects.filter(is_active=True).prefetch_related('tipoInsumo').all()
        # serializer
        serializer_class = serializer.InsumoTipoInsumoWithoutEstado(insumo, many=True)
        return Response(serializer_class.data)

    def create(self, request):
        print(request.data)
        serializer_class = serializer.InsumoSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save(created_by=request.user)
        return Response(serializer_class.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        try:
            insumo = models.Insumo.objects.get(id=pk)
            insumo.is_active_(raise_exception=True, msg='Insumo no existente')
            serializer_class = serializer.InsumoTipoInsumoSerializer(insumo)
            return Response(serializer_class.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            insumo = models.Insumo.objects.get(id=pk)
            insumo.is_active_(raise_exception=True, msg='Insumo no existente')
            serializer_class = serializer.InsumoSerializer(insumo, data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            insumo = models.Insumo.objects.get(id=pk)
            insumo.codigo = create_hash(insumo.id,insumo.codigo)
            insumo.is_active_(raise_exception=True, msg='Insumo no existente')
            insumo.is_active = False
            insumo.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response({"error": "No se puede eliminar porque existe una dependencia con otro elemento"}, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

class OrdenRetiroCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def __table__():
        return 'ordenretiro'

    def list(self, request):
        # join
        orden_retiro = models.OrdenRetiro.objects.filter(is_active=True).all()
        # serializer
        serializer_class = serializer.OrdenRetiroFkReplacedSerializer(orden_retiro, many=True)
        return Response(serializer_class.data)

    @transaction.atomic
    def create(self, request):
        try:
            serializer_class = InventarioCommonLogic.create_orden_retiro(request.data, request.user)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            orden_retiro = models.OrdenRetiro.objects.get(id=pk)
            orden_retiro.is_active_(raise_exception=True, msg='Orden de retiro no existente')
            serializer_class = serializer.OrdenRetiroFkReplacedSerializer(orden_retiro)
            return Response(serializer_class.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        return Response({"error": "La actualización no está permitida"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk):
        return Response({"error": "La eliminación no está permitida"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AjusteStockCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def __table__():
        return 'ajustestock'
    
    def list(self, request):
        # join
        ajuste_stock = models.AjusteStock.objects.all()
        # serializer
        serializer_class = serializer.AjusteStockJoinedSerializer(ajuste_stock, many=True)
        return Response(serializer_class.data)

    @transaction.atomic
    def create(self, request):
        try:
            serializer_class = serializer.AjusteStockSerializer(data=request.data)

            serializer_class.is_valid(raise_exception=True)
            serializer_class.save(created_by=request.user)
            # update cantidad from Insumo
            insumo = models.Insumo.objects.get(id=request.data.get('insumo'))
            
            ## check positive value
            if int(request.data.get('cantidad')) <= 0:
                raise Exception("Negative or zero quantity")

            ## sum quantities
            if request.data.get('accionCantidad') == models.ActionScale.SUMAR:
                quant = insumo.cantidad + int(request.data.get('cantidad'))
            else:
                quant = insumo.cantidad - int(request.data.get('cantidad'))

            # check quant
            if quant < 0:
                raise Exception("Excedeed Quantity")

            insumo.cantidad = quant
            insumo.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            ajuste_stock = models.AjusteStock.objects.get(id=pk)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_class = serializer.AjusteStockJoinedSerializer(ajuste_stock)
        return Response(serializer_class.data)

    def update(self, request, pk):
        return Response({"error": "La actualización no está permitida"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk):
        return Response({"error": "La eliminación no está permitida"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
