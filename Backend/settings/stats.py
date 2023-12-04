from django.db import connection
from settings.common_class import LoginRequiredNoRedirect
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import inventario.models as inv_models

class CustomViewSet(ViewSet):
    permission_classes = [IsAdminUser]

def toObjList(resultados):
    keys = resultados.pop(0);
    return [dict(zip(keys,item)) for item in resultados]

class InsumosBajoReposición(LoginRequiredNoRedirect, CustomViewSet):
    def list(self, request):
        #insumos = inv_models.Insumo.objects.aggregate(total_consumido=Sum('precio')
        query = """
                WITH tmp AS (SELECT id, nombre,tipoInsumo_id, cantidad , puntoReposicion FROM inventario_insumo
                WHERE cantidad <= puntoReposicion
                ORDER BY id DESC
                LIMIT 10)
                SELECT 
                tmp.id,
                tmp.nombre AS name,
                inventario_tipoinsumo.nombre AS type,
                tmp.cantidad AS value,
                tmp.puntoReposicion AS repositionValue 
                FROM tmp INNER JOIN inventario_tipoinsumo
                ON tmp.tipoInsumo_id=inventario_tipoinsumo.id
                LIMIT 10
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()
        return Response(toObjList(resultados))

class TareasPendientesUrgentes(LoginRequiredNoRedirect, CustomViewSet):
    def list(self, request):
        query = """
                    SELECT 
                    fechaGeneracion as fecha,
                    prioridad,
                    categoria,
                    estado,
                    tarea_sector.nombre as sector,
                    tarea_sector.edificio as edificio
                    FROM tarea_ordenservicio
                    INNER JOIN tarea_sector
                    ON tarea_ordenservicio.sector_id=tarea_sector.id 
                    ORDER BY 
                        CASE prioridad 
                        WHEN "CRITICO" THEN 1
                        WHEN "URGENTE" THEN 2
                        WHEN "NORMAL" THEN 3
                        END ASC,
                        CASE estado
                        WHEN "EN_ESPERA" THEN 1
                        WHEN "EN_PROGRESO" THEN 2
                        WHEN "APROBADO" THEN 3
                        END ASC
                    LIMIT 10
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(toObjList(resultados))

class InsumoMasConsumido(LoginRequiredNoRedirect, CustomViewSet):
    def list(self, request):
        query = """
                SELECT 
                inventario_insumo.id,
                inventario_insumo.nombre,
                unidadMedida,
                codigo AS codigoInsumo,
                inventario_tipoinsumo.nombre AS tipoInsumo,
                SUM(inventario_ordenretiro.cantidad) AS cantidadTotal
                FROM inventario_insumo
                INNER JOIN inventario_ordenretiro 
                ON inventario_insumo.id=inventario_ordenretiro.insumo_id
                INNER JOIN inventario_tipoinsumo
                ON inventario_insumo.tipoinsumo_id=inventario_tipoinsumo.id
                GROUP BY inventario_insumo.id
                ORDER BY cantidadTotal
                LIMIT 6
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(toObjList(resultados))

class TareasCompletadas(LoginRequiredNoRedirect, CustomViewSet):
    def list(self, request):
        ## filtrar por nulos fechaFin
        query = """
            SELECT 
            DATE_FORMAT(fechaFin, '%M') AS name,
            COUNT(*) AS value
            FROM tarea_tarea
            INNER JOIN tarea_ordenservicio 
            ON tarea_ordenservicio.id = tarea_tarea.ordenServicio_id
            WHERE YEAR(fechaFin) = YEAR(CURDATE())
            AND tarea_ordenservicio.estado = "FINALIZADA"
            GROUP BY name;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(toObjList(resultados))


class EmpleadosHorasTotales(LoginRequiredNoRedirect, CustomViewSet):
    def list(self, request):
        query = """
            WITH tmp AS (
                SELECT 
                empleado_id, 
                SUM(horasEstimadas) AS total_estimadas, 
                SUM(horasTotales) AS total_reales
                FROM tarea_tiempo
                GROUP BY empleado_id
            )
            SELECT nombre, apellido, tmp.total_estimadas, tmp.total_reales
            FROM tmp INNER JOIN tarea_empleado
            ON tmp.empleado_id=tarea_empleado.id
            ORDER BY total_estimadas DESC, total_reales DESC
            LIMIT 5
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(toObjList(resultados))
