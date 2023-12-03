from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from herramienta.views import HerramientaCommonLogic
from inventario.views import InventarioCommonLogic
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from settings.common_class import LoginRequiredNoRedirect
from . import serializer
from . import models
import herramienta.models as herramienta_models
import inventario.models as inventario_models
import inventario.serializer as inventario_serializer
import json

class CustomModelViewSet(LoginRequiredNoRedirect, viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'put', 'delete']

class TareaCommonLogic:
    def update_herramientas(herramientas_data, tarea, status=None):
        # update herramientas and estado
        for herramienta_data in herramientas_data:
            
            ## update herramienta
            herramienta = herramienta_models.Herramienta.objects.get(id=int(herramienta_data['herramienta']))
            tarea.herramientas.add(herramienta)
            if not herramienta.is_available():
                raise Exception('La herramienta no está disponible')

            if status is None:
                herramienta.estado = herramienta_data['estado']
            else:
                herramienta.estado = status

            herramienta.save()

            ## create estado entry
            HerramientaCommonLogic.create_estado_entry(herramienta)

    def create_entry_insumos(insumos_data, tarea_pk, user):
        for insumo_data in insumos_data:
            insumo_data['tarea'] = tarea_pk
            InventarioCommonLogic.create_orden_retiro(insumo_data, user)

    # forgive me, God, this aberration, but I'm in a hurry and I'm drunk
    def update_insumos(insumos_data, tarea, user):
        ordenes_retiro = inventario_models.OrdenRetiro.objects.filter(tarea=tarea):
        for insumo_data in insumos_data:
            # get orden with insumo
            insumo_existent = ordenes_retiro.filter(insumo=insumo_data['id']).first()

            if insumo_existent is None:
                # create order
                insumo_data['tarea'] = tarea_pk
                InventarioCommonLogic.create_orden_retiro(insumo_data, user)
            else: 
                insumo_data_cant = int(insumo_data['cantidad'])
                if insumo_data_cant == 0:
                    # return insumos
                    insumo_existent.insumo.cantidad += insumo_existent.cantidad
                    insumo_existent.insumo.save()
                    # delete orden
                    insumo_existent.delete()

                elif insumo_data_cant != insumo_existent.cantidad:
                    # update quantities
                    diff = insumo_existent.cantidad - insumo_data_cant
                    insumo_existent.cantidad = insumo_data_cant
                    insumo_existent.insumo.cantidad += diff

                    # validate and check
                    insumo_existent.save(created_by=user)
                    insumo_existent.insumo.save()

    def create_empleados_relation(empleados_data, tarea_pk, user):
        for empleado in empleados_data:

            ## dict tiempo entry
            tiempo_entry = {}
            tiempo_entry['empleado'] = empleado['empleado']
            tiempo_entry['tarea'] = tarea_pk
            tiempo_entry['horasEstimadas'] = empleado.get('horasEstimadas')
            if empleado.get('responsable') is not None:
                tiempo_entry['responsable'] = empleado.get('responsable')

            ## serializer
            tiempo_serializer = serializer.TiempoSerializer(data=tiempo_entry)
            tiempo_serializer.is_valid(raise_exception=True)
            ## saving
            tiempo_serializer.save(created_by=user)

    def update_empleados_relation(empleados_data, tarea_pk, user):
        tarea_empleados = models.Tiempo.objects.filter(tarea=tarea_pk).all()
        new_empleados = []

        # update empleados
        for empleado in empleados_data:
            tiempo_model = next((model for model in tarea_empleados if model.empleado == empleado['id']), None)
            if tiempo_model is None:
                new_empleados.append(empleado)
            else:
                if 'horasEstimadas' in empleado:
                    tiempo_model.horasEstimadas = empleado['horasEstimadas']
                if 'horasTotales' in empleado:
                    tiempo_model.horasTotales = empleado['horasTotales']
                if 'responsable' in empleado:
                    tiempo_model.responsable = empleado['responsable']
                tiempo_model.save()

        # add empleados
        if not new_empleados:
            create_empleados_relation(new_empleados, tarea_pk, user)

    def restore_herramientas(tarea, user):
        # restore herramientas
        for herramienta in tarea.herramientas.all():
            herramienta.estado = herramienta_models.StatusScale.DISPONIBLE
            herramienta.save()
            # create entry in EstadoHerramienta
            estado = herramienta_models.EstadoHerramienta(
                    herramienta=herramienta,
                    estado=herramienta_models.StatusScale.DISPONIBLE,
                    observaciones='Eliminacion de tarea id '+str(pk),
                    created_by=user
                )
            estado.save()

    def restore_insumos(tarea, user):
        # restore insumos
        for orden_retiro in tarea.insumos_retirados.all():
            ajuste_stock = inventario_models.AjusteStock(
                    insumo=orden_retiro.insumo,
                    cantidad=orden_retiro.cantidad,
                    observaciones='Eliminacion de tarea id '+str(pk),
                    accionCantidad=inventario_models.ActionScale.SUMAR,
                    created_by=user
                )
            ajuste_stock.save()

    def restore_empleados(tarea):
        # restore empleados, delete Tiempo entry
        for tiempo in models.Tiempo.objects.filter(tarea=tarea):
            tiempo.delete()

    def deactivate_tarea(tarea, user):
        # restore herramientas
        TareaCommonLogic.restore_herramientas(tarea, user)

        # restore insumos
        TareaCommonLogic.restore_insumos(tarea, user)

        # restore empleados, delete Tiempo entry
        TareaCommonLogic.restore_empleados(tarea)

        tarea.is_active = False

class EmpleadoCRUD(CustomModelViewSet):
    serializer_class = serializer.EmpleadoSerializer
    queryset = models.Empleado.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save(created_by=request.user)

            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        empleado = self.get_object()

        # check
        if not empleado.is_active:
            raise ObjectDoesNotFound('Empleado inactivo')

        # it is assigned?
        for tiempo in models.Tiempo.objects.filter(empleado=empleado):
            if tiempo.tarea.fechaFin is not None:
                raise Exception('Empleado no puede eliminarse porque está asignado a una tarea sin finalizar')

        # deactivate empleado
        empleado.is_active = False
        empleado.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def __table__():
        return 'empleado'

class EncuestaSatisfaccionCRUD(CustomModelViewSet):
    serializer_class = serializer.EncuestaSatisfaccionSerializer
    queryset = models.EncuestaSatisfaccion.objects.all()

    def __table__():
        return 'encuestasatisfaccion'

class TareaCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):

    def __table__():
        return 'tarea'

    def list(self, request):
        try:
            # join
            tarea = models.Tarea.objects.prefetch_related('empleados', 'herramientas').all()
            # serializer
            serializer_class = serializer.TareaJoinedSerializer(tarea, many=True, read_only=False)

            # inverse relation (get OrdenRetiro)
            for tarea_instance in tarea:
                ordenes_retiro = tarea_instance.insumos_retirados.all()
                
                tarea_data = next(tarea_data 
                                  for tarea_data in serializer_class.data 
                                  if tarea_data['id'] == tarea_instance.id)
                
                tarea_data['retiros_insumos'] = [
                        {'insumo': orden_retiro.insumo.nombre,
                         'fechaHora': orden_retiro.fechaHora,
                         'cantidad': orden_retiro.cantidad} for orden_retiro in ordenes_retiro
                ]
            return Response(serializer_class.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def create(self, request):
        try:
            # get empleados, herramientas, insumos
            to_create = request.data.copy()
            empleados_data = json.loads(to_create.pop('empleados', [])[0])
            herramientas_data = json.loads(to_create.pop('herramientas', [])[0])
            insumos_data = json.loads(to_create.pop('retiros_insumos', [])[0])
            orden_servicio_pk = json.loads(to_create.get('orden_servicio', [])[0])
            orden_servicio_model = models.OrdenServicio.objects.get(id=orden_servicio_pk)
            
            # check previous tarea
            for tarea_iter in models.Tarea.objects.filter(ordenServicio=orden_servicio_model):
                if tarea_iter.is_active:
                    raise Exception("Orden de servicio ya tiene una tarea adjunta")

            # check and create tarea
            serializer_tarea = serializer.TareaSerializer(data=to_create)
            serializer_tarea.is_valid(raise_exception=True)
            tarea = serializer_tarea.save(created_by=request.user)
               
            # create empleados relation (Tiempo)
            TareaCommonLogic.create_empleados_relation(empleados_data, tarea.id, request.user)
            
            # update herramientas and estado
            TareaCommonLogic.update_herramientas(herramientas_data, tarea, herramienta_models.StatusScale.EN_USO)
            
            # update insumos
            TareaCommonLogic.create_entry_insumos(insumos_data, tarea.id, request.user)
            
            # update orden servicio
            tarea.ordenServicio = orden_servicio_model

            # modify orden servicio status
            if tarea.fechaInicio == timezone.now().date():
                orden_servicio_model.estado = models.OrdenServicio().StatusScale.EN_PROGRESO
            else:
                orden_servicio_model.estado = models.OrdenServicio().StatusScale.APROBADA

            orden_servicio_model.save()
            tarea.save()

            return Response(serializer_tarea.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            print(request.user.id)
            tarea = models.Tarea.objects.get(id=pk)
            tarea_data = serializer.TareaJoinedSerializer(tarea).data.copy()

            # insumos asociados
            insumos = []
            for orden_retiro in tarea.insumos_retirados.all():
                insumoRetiro = {}
                insumo = orden_retiro.insumo
                insumoRetiro['insumo'] = insumo.nombre
                insumoRetiro['id_insumo'] = insumo.id
                insumoRetiro['fechaHora'] = orden_retiro.fechaHora
                insumoRetiro['cantidad'] = orden_retiro.cantidad
                insumos.append(insumoRetiro)
            
            # add tiempos de empleados
            ## esto es una cagada, ineficiente
            empleados = tarea_data['empleados']
            for tiempo in models.Tiempo.objects.filter(tarea=tarea):
                for emp in empleados:
                    if emp['id'] == tiempo.empleado.id:
                        emp['horasEstimadas'] = tiempo.horasEstimadas
                        emp['horasTotales'] = tiempo.horasTotales
                        emp['responsable'] = tiempo.responsable

            tarea_data['retiros_insumos'] = insumos
            return Response(tarea_data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, pk):
        try:
            tarea_update_data = request.data.copy()
            herramientas_data = tarea_update_data.pop('herramientas', [])
            empleados_data = tarea_update_data.pop('empleados', [])
            insumos_data = tarea_update_data.pop('retiros_insumos', [])

            tarea = models.Tarea.objects.get(id=pk)
            tarea_serializer = serializer.TareaSerializer(tarea, data=tarea_update_data)
            tarea_serializer.is_valid(raise_exception=True)
            tarea_serializer.save()

            # update herramientas and estado
            TareaCommonLogic.update_herramientas(herramientas_data, tarea)

            # update empleados relation (Tiempo)
            TareaCommonLogic.update_empleados_relation(empleados_data, tarea.id, request.user)

            # update insumos
            TareaCommonLogic.update_insumos(insumos_data, tarea, request.user)

            # update orden servicio
            if tarea.fechaFin is not None:
                tarea.ordenServicio.estado = models.OrdenServicio().StatusScale.FINALIZADA
                tarea.ordenServicio.save()

            return Response(tarea_serializer.data)
        except ObjectDoesNotExist: 
            transaction.set_rollback(True)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, pk):
        try:
            tarea = models.Tarea.objects.get(id=pk)

            # check if it is active
            if not tarea.is_active:
                raise ObjectDoesNotExist('Tarea no encontrada para eliminación')

            # check if tarea is finished
            if tarea.fechaFin is not None:
                raise Exception('No puede eliminarse esta tarea porque ya está finalizada')

            # update status in OrdenServicio
            tarea.ordenServicio.estado = models.OrdenServicio().StatusScale.APROBADA
            tarea.ordenServicio.save()

            TareaCommonLogic.deactivate_tarea(tarea, request.user)
            tarea.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist: 
            transaction.set_rollback(True)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class OrdenServicioCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):

    def __table__():
        return 'ordenservicio'

    def list(self, request):
        # join
        orden_servicio = models.OrdenServicio.objects.prefetch_related('usuario', 'sector').all()
        # serializer
        serializer_class = serializer.OrdenServicioUsuarioSerializer(orden_servicio, many=True)
        return Response(serializer_class.data)

    def create(self, request):
        try:
            serializer_class = serializer.OrdenServicioSerializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save(usuario=request.user)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            orden_servicio = models.OrdenServicio.objects.get(id=pk)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer_class = serializer.OrdenServicioUsuarioSerializer(orden_servicio)
        return Response(serializer_class.data)

    def update(self, request, pk):
        try:
            orden_servicio = models.OrdenServicio.objects.get(id=pk)
            serializer_class = serializer.OrdenServicioSerializer(orden_servicio, data=request.data)
            serializer_class.is_valid(raise_exception=True)
            # check status
            orden_servicio.clean(serializer_class.validated_data['estado'])
            serializer_class.save()
            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, pk):
        try:
            orden_servicio = models.OrdenServicio.objects.get(id=pk)

            # check if it is active
            if not orden_servicio.is_active:
                raise ObjectDoesNotExist('Orden de servicio no encontrada para eliminación')

            # check orden servicio
            if orden_servicio.estado in [orden_servicio.StatusScale.EN_PROGRESO,
                                         orden_servicio.StatusScale.FINALIZADA]:
                raise Exception('Orden de servicio en progreso o finalizada, no puede eliminarse')

            # check tarea progress
            for tarea in models.Tarea.objects.get(ordenServicio=orden_servicio):
                if tarea.is_active:
                    TareaCommonLogic.deactivate_tarea(tarea, request.user)
                    tarea.save()

            orden_servicio.is_active = False

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist: 
            transaction.set_rollback(True)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SectorListCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):
    def __table__():
        return 'sector'

    def retrieve(self, request, nombre):
        try:
            sectores = models.Sector.objects.filter(edificio=nombre).all()
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer_class = serializer.SectorSubsectorSerializer(sectores, many=True)
        return Response(serializer_class.data)
    
class SectorCRUD(CustomModelViewSet):
    serializer_class = serializer.SectorSerializer
    queryset = models.Sector.objects.all()

    def __table__():
        return 'sector'

class TiempoCRUD(CustomModelViewSet):
    serializer_class = serializer.TiempoSerializer
    queryset = models.Tiempo.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save(created_by=request.user)

            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
