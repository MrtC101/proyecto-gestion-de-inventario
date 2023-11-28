from django.db import connection
from settings.common_class import LoginRequiredNoRedirect
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import inventario.models as inv_models

class InsumosMasConsumidos(LoginRequiredNoRedirect, ViewSet):
    def list(self, request):
        #insumos = inv_models.Insumo.objects.aggregate(total_consumido=Sum('precio')
        query = """
            WITH tmp AS (
            SELECT insumo_id, SUM(cantidad) AS total_consumido, strftime('%W', fechaHora) as semana
            FROM inventario_ordenretiro
            WHERE strftime('%Y', fechaHora)=strftime('%Y', date('now'))
            GROUP BY semana, insumo_id
            ORDER BY semana DESC, total_consumido DESC
            )
            SELECT inventario_insumo.nombre, tmp.*
            FROM tmp INNER JOIN inventario_insumo
                ON tmp.insumo_id=inventario_insumo.id
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()
        
        return Response(resultados)

class TiposInsumoMasUtilizados(LoginRequiredNoRedirect, ViewSet):
    def list(self, request):
        query = """
            WITH tmp AS (
            SELECT tipoInsumo_id, COUNT(tipoInsumo_id) AS total_tipos
            FROM inventario_insumo
            GROUP BY tipoInsumo_id
            LIMIT 10
            )
            SELECT inventario_tipoinsumo.nombre, tmp.*
            FROM tmp INNER JOIN inventario_tipoinsumo
                ON tmp.tipoInsumo_id=inventario_tipoinsumo.id
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(resultados)

class EmpleadosHorasTotales(LoginRequiredNoRedirect, ViewSet):
    def list(self, request):
        query = """
            WITH tmp AS (
            SELECT empleado_id, SUM(horasEstimadas) total_estimadas, SUM(horasTotales) total_reales
            FROM tarea_tiempo
            GROUP BY empleado_id
            )
            SELECT nombre, apellido, tmp.*
            FROM tmp INNER JOIN tarea_empleado
                ON tmp.empleado_id=tarea_empleado.id
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(resultados)

class TareasCompletadas(LoginRequiredNoRedirect, ViewSet):
    def list(self, request):
        ## filtrar por nulos fechaFin
        query = """
            SELECT strftime('%W', fechaFin) AS semana, COUNT(*) AS total
            FROM tarea_tarea
            WHERE strftime('%Y', fechaFin)=strftime('%Y', date('now'))
            GROUP BY semana
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(resultados)