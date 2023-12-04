from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from settings.common_class import LoginRequiredNoRedirect
from settings.auxs_fn import ErrorToString, create_hash

from . import serializer
from . import models

import json
import random
import string

class CustomModelViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'put', 'delete']
    permission_classes = [IsAdminUser]

class UsuarioCRUD(LoginRequiredNoRedirect, CustomModelViewSet):
    serializer_class = serializer.UsuarioSerializer
    queryset = models.Usuario.objects.all().filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'update', 'delete']:
            return serializer.UsuarioSerializerNoPassword
        return serializer.UsuarioSerializer
   
    @transaction.atomic
    def create(self, request):
        try:
            #invalid_data = request.data.copy()
            #invalid_data["username"] = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            #invalid_data["password"] = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            usuario_serializer = serializer.UsuarioSerializer(data=request.data)
            usuario_serializer.is_valid(raise_exception=True)
            usuario_serializer.validated_data['password'] = make_password(usuario_serializer.validated_data['password'])
            user = usuario_serializer.save(is_active=True, default_password=True)
            
            # add to group
            if user.is_staff:
                grupo = Group.objects.get(name='staff_users')
            else:
                grupo = Group.objects.get(name='regular_users')

            grupo.user_set.add(user)
            grupo.save()

            user_return = usuario_serializer.data.copy()
            user_return.pop('password')
            return Response(user_return, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            user_instance = self.get_object()

            if not user_instance.is_active:
                raise ObjectDoesNotExist()

            user_serializer = self.get_serializer(user_instance, data=request.data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            self.perform_update(user_serializer)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            user_instance = self.get_object()    
            # check if it is active
            if not user_instance.is_active:
                raise ObjectDoesNotExist('Usuario no encontrado para eliminación')
            user_instance.username = create_hash(user_instance.id,user_instance.username);
            user_instance.legajo = None;
            user_instance.is_active = False
            user_instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e: 
            return Response({'error': ErrorToString(e)}, status=status.HTTP_400_BAD_REQUEST)

    def __table__():
        return 'usuario'

@csrf_exempt
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    #response.set_cookie('csrftoken', get_token(request),samesite='None')
    return response

@csrf_exempt
@require_POST
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in.'})

@csrf_exempt
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})

class SessionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return JsonResponse({'isAuthenticated': True})

class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    @csrf_exempt
    def get(request, format=None):
        if request.user.is_staff:
            rol = "Administrador" if request.user.is_superuser else "Staff"
        else:
            rol = "Regular"
        return JsonResponse({'username': request.user.username,
                             'id': request.user.id,
                             'email': request.user.email,
                             'default_password': request.user.default_password,
                             'is_staff': request.user.is_staff,
                             'rol': rol})

class PasswordView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, format=None):
        try:
            if not check_password(request.data.get('password'), request.user.password):
                raise Exception('Invalid current password')

            request.user.password = make_password(request.data['new_password'])
            request.user.default_password = False
            request.user.save()
            update_session_auth_hash(request, request.user)
            return Response({'notice': 'password changed'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'isAuthenticated': True})
