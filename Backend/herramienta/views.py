from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from settings.common_class import LoginRequiredNoRedirect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializer
from . import models
from settings.auxs_fn import ErrorToString, create_hash
from rest_framework.exceptions import APIException

class CustomModelViewSet(LoginRequiredNoRedirect, viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'put', 'delete']
    permission_classes = [IsAdminUser]

class HerramientaCommonLogic:
    def create_estado_entry(herramienta):
        # estado creation
        estado_data = {'herramienta': herramienta.id,
                       'fecha': herramienta.fechaAlta,
                       'estado': herramienta.estado,
                       'observaciones': 'Alta de herramienta',
                       'created_by': herramienta.created_by.id}
        estado_serializer = serializer.EstadoHerramientaSerializer(data=estado_data)
        estado_serializer.is_valid(raise_exception=True)
        estado_serializer.save(created_by=herramienta.created_by)

class TipoHerramientaCRUD(CustomModelViewSet):
    serializer_class = serializer.TipoHerramientaSerializer
    queryset = models.TipoHerramienta.objects.all()

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
            tipo_herramienta = models.TipoHerramienta.objects.get(id=pk)
            tipo_herramienta.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response({"error": "No se puede eliminar porque existe una dependencia con otro elemento"}, status=status.HTTP_409_CONFLICT)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)

    def __table__():
        return 'tipoherramienta'

class HerramientaCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def __table__():
        return 'herramienta'

    def list(self, request):
        # join
        herramienta = models.Herramienta.objects \
                        .filter(is_active=True) \
                        .prefetch_related('tipoHerramienta').all()
        # serializer
        serializer_class = serializer.HerramientaJoinedSerializer(herramienta, many=True)
        return Response(serializer_class.data)

    @transaction.atomic
    def create(self, request):
        try:
            serializer_class = serializer.HerramientaSerializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            
            herramienta = serializer_class.save(created_by=request.user)    

            # cannot create herramienta with estado eliminado
            if herramienta.estado != models.StatusScale.DISPONIBLE:
                raise Exception('No se puede crear una herramienta con estado que no sea disponible')
            
            # estado creation
            HerramientaCommonLogic.create_estado_entry(herramienta)

            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            herramienta = models.Herramienta.objects.get(id=pk)
            herramienta.is_active_(raise_exception=True, msg='Herramienta no existente')
            serializer_class = serializer.HerramientaJoinedSerializer(herramienta)
            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            herramienta = models.Herramienta.objects.get(id=pk)

            # herramienta is active
            herramienta.is_active_(raise_exception=True, msg='Herramienta no encontrada para eliminación')

            # check if it is in use
            last_estado = models.EstadoHerramienta.objects.filter(herramienta=herramienta).latest('fecha')
            if last_estado.estado == models.StatusScale.EN_USO:
                raise Exception('No es posible cambiar estado mientras está en uso por una tarea')

            # create estado entry
            estado_herramienta = models.EstadoHerramienta(
                    herramienta=herramienta,
                    estado=request.data['estado'],
                    observaciones='Actualizacion estado herramienta id '+str(pk),
                    created_by=request.user
                )
            estado_herramienta.save()

            serializer_class = serializer.HerramientaSerializer(herramienta, data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, pk):
        try:
            herramienta = models.Herramienta.objects.get(id=pk)

            # herramienta is active
            herramienta.is_active_(raise_exception=True, msg='Herramienta no encontrada para eliminación')

            # check if it is in use
            last_estado = models.EstadoHerramienta.objects.filter(herramienta=herramienta).latest('fecha')
            if last_estado.estado == models.StatusScale.EN_USO:
                raise Exception('No es posible eliminar: está en uso')
            
            # create estado entry
            estado_herramienta = models.EstadoHerramienta(
                    herramienta=herramienta,
                    estado=models.StatusScale.ELIMINADA,
                    observaciones='Eliminacion de registro herramienta id '+str(pk),
                    created_by=request.user
                )
            estado_herramienta.save()

            # deactivate herramienta
            herramienta.codigo = create_hash(herramienta.id,herramienta.codigo)
            herramienta.estado = models.StatusScale.ELIMINADA
            herramienta.is_active = False
            herramienta.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist: 
            transaction.set_rollback(True)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            transaction.set_rollback(True)
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

class EstadoHerramientaCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def __table__():
        return 'estadoherramienta'

    def list(self, request):
        # join
        estado_herramienta = models.EstadoHerramienta.objects.filter(is_active=True).all()
        # serializer
        serializer_class = serializer.EstadoHerramientaJoinedSerializer(estado_herramienta, many=True)
        return Response(serializer_class.data)

    @transaction.atomic
    def create(self, request):
        try:
            serializer_class = serializer.EstadoHerramientaSerializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            estado = serializer_class.save(created_by=request.user)

            # update estado from Herramienta
            herramienta = models.Herramienta.objects.get(id=estado.herramienta.id)
            herramienta.estado = estado.estado
            herramienta.save()

            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            estado_herramienta = models.EstadoHerramienta.objects.get(id=pk)
            estado_herramienta.is_active_(raise_exception=True, msg='Estado de herramienta no existente')
            serializer_class = serializer.EstadoHerramientaJoinedSerializer(estado_herramienta)
            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            estado_herramienta = models.EstadoHerramienta.objects.get(id=pk)
            estado_herramienta.is_active_(raise_exception=True, msg='Estado de herramienta no existente')
            serializer_class = serializer.EstadoHerramientaSerializer(estado_herramienta, data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        return Response({"error": "La eliminación no está permitida"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
