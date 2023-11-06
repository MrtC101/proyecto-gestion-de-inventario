from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from settings.common_class import LoginRequiredNoRedirect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializer
from . import models

class CustomModelViewSet(LoginRequiredNoRedirect, viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'put', 'delete']

class HerramientaCommonLogic:
    def create_estado_entry(herramienta):
        # estado creation
        estado_data = {'herramienta': herramienta.id,
                       'fecha': herramienta.fechaAlta,
                       'estado': herramienta.estado,
                       'observaciones': 'Alta de herramienta'}
        estado_serializer = serializer.EstadoHerramientaSerializer(data=estado_data)
        estado_serializer.is_valid(raise_exception=True)
        estado_serializer.save()

class TipoHerramientaCRUD(CustomModelViewSet):
    serializer_class = serializer.TipoHerramientaSerializer
    queryset = models.TipoHerramienta.objects.all()

    def __table__():
        return 'tipoherramienta'

class HerramientaCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):

    def __table__():
        return 'herramienta'

    def list(self, request):
        # join
                        #.filter(estado='OK') \
        herramienta = models.Herramienta.objects \
                        .prefetch_related('tipoHerramienta').all()
        # serializer
        serializer_class = serializer.HerramientaJoinedSerializer(herramienta, many=True)
        return Response(serializer_class.data)

    @transaction.atomic
    def create(self, request):
        try:
            serializer_class = serializer.HerramientaSerializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            herramienta = serializer_class.save()

            # estado creation
            HerramientaCommonLogic.create_estado_entry(herramienta)

            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            herramienta = models.Herramienta.objects.get(id=pk)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_class = serializer.HerramientaJoinedSerializer(herramienta)
        return Response(serializer_class.data)

    def update(self, request, pk):
        try:
            herramienta = models.Herramienta.objects.get(id=pk)
            serializer_class = serializer.HerramientaSerializer(herramienta, data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            herramienta = models.Herramienta.objects.get(id=pk)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)

        herramienta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EstadoHerramientaCRUD(LoginRequiredNoRedirect, viewsets.ViewSet):

    def __table__():
        return 'estadoherramienta'

    def list(self, request):
        # join
        estado_herramienta = models.EstadoHerramienta.objects.all()
        # serializer
        serializer_class = serializer.EstadoHerramientaJoinedSerializer(estado_herramienta, many=True)
        return Response(serializer_class.data)

    @transaction.atomic
    def create(self, request):
        try:
            serializer_class = serializer.EstadoHerramientaSerializer(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            estado = serializer_class.save()

            # update estado from Herramienta
            herramienta = models.Herramienta.objects.get(id=estado.herramienta.id)
            herramienta.estado = estado.estado
            herramienta.save()

            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            estado_herramienta = models.EstadoHerramienta.objects.get(id=pk)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_class = serializer.EstadoHerramientaJoinedSerializer(estado_herramienta)
        return Response(serializer_class.data)

    def update(self, request, pk):
        try:
            estado_herramienta = models.EstadoHerramienta.objects.get(id=pk)
            serializer_class = serializer.EstadoHerramientaSerializer(estado_herramienta, data=request.data)
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        estado_herramienta = models.EstadoHerramienta.objects.get(id=pk)
        estado_herramienta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
