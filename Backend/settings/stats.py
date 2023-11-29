from django.db import connection
from settings.common_class import LoginRequiredNoRedirect
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import inventario.models as inv_models

def toObjList(resultados):
    keys = resultados.pop(0);
    return [dict(zip(keys,item)) for item in resultados]
    

class InsumosBajoReposición(LoginRequiredNoRedirect, ViewSet):
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

class TareasPendientesUrgentes(LoginRequiredNoRedirect, ViewSet):
    def list(self, request):
        query = """
                    SELECT 
                    tarea_tarea.id,
                    tarea_tarea.tipo,
                    tarea_tarea.clasificacion,
                    tarea_sector.edificio AS edificio,
                    tarea_sector.nombre AS sector,
                    prioridad,
                    estado
                    FROM tarea_tarea
                    INNER JOIN tarea_ordenservicio
                    ON tarea_tarea.id=tarea_ordenservicio.tarea_id
                    INNER JOIN tarea_sector
                    ON tarea_ordenservicio.sector_id=tarea_sector.id 
                    WHERE estado = "EN_ESPERA" 
                    OR estado = "APROBADO"
                    OR estado = "EN_PROGRESO"
                    ORDER BY 
                        CASE prioridad 
                        WHEN "CRITICO" THEN 1
                        WHEN "URGENTE" THEN 2
                        WHEN "NORMAL" THEN 3
                        END ASC,
                        CASE estado
                        WHEN "EN_PROGRESO" THEN 1
                        WHEN "APROBADO" THEN 2
                        WHEN "EN_ESPERA" THEN 3
                        END ASC
                    LIMIT 10
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(toObjList(resultados))

class InsumoMasConsumido(LoginRequiredNoRedirect, ViewSet):
    def list(self, request):
        query = """
                SELECT 
                inventario_insumo.id,
                inventario_insumo.nombre,
                unidadMedida,
                codigo AS codigoInsumo,
                inventario_tipoinsumo.nombre AS tipoInsumo,
                SUM(inventario_ordenRetiro.cantidad) AS cantidadTotal
                FROM inventario_insumo
                INNER JOIN inventario_ordenRetiro 
                ON inventario_insumo.id=inventario_ordenRetiro.insumo_id
                INNER JOIN inventario_tipoinsumo
                ON inventario_insumo.tipoinsumo_id=inventario_tipoinsumo.id
                GROUP BY inventario_insumo.id
                ORDER BY cantidadTotal
                LIMIT 10
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(toObjList(resultados))

class TareasCompletadas(LoginRequiredNoRedirect, ViewSet):
    def list(self, request):
        ## filtrar por nulos fechaFin
        query = """
            SELECT strftime('%W', fechaFin) AS semana, COUNT(*) AS total
            FROM tarea_tarea
            INNER JOIN tarea_ordenservicio
            ON tarea_ordenservicio.tarea_id=tarea_tarea.id
            WHERE strftime('%Y', fechaFin)=strftime('%Y', date('now'))
            AND tarea_ordenservicio.estado="FINALIZADA"
            GROUP BY semana
            LIMIT 10
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultados = [[descrip[0] for descrip in cursor.description]]
            resultados += cursor.fetchall()

        return Response(toObjList(resultados))


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

        return Response(toObjList(resultados))
