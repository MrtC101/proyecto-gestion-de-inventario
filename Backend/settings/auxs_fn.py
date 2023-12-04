import hashlib
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import inspect
import inventario.models as inv
import tarea.models as tar
import compra.models as com
import herramienta.models as her
import usuario.models as usu

from rest_framework.exceptions import APIException

def ErrorToString(e):
    msg = "";
    if(isinstance(e,APIException)):
        if(hasattr(e,'detail')):
            for key in e.detail.keys():
                for err in e.detail[key]:
                    msg+= key+":"+str(err)+"\n"
        else:
            msg=str(e.default_detail)
    else:
        msg = str(e);
    return msg;

def create_hash(id, val):
    data_to_hash = f"{id}-{val}"
    hashed_value = hashlib.sha256(data_to_hash.encode()).hexdigest()[:8]
    return hashed_value

@login_required
def get_models(request):
    """
    Captures names of apps, models and their attributes

    :return: dict with fields
    """

    if not request.user.is_staff:
        return JsonResponse({"error": "No puedes acceder a esta url"},status=403)

    # Get apps
    apps_names = ["inventario", "compra", "usuario", "tarea", "herramienta"]

    models_dict = {}
    for _ in apps_names:
        app = apps.get_app_config(_)
        models = app.get_models()
        tables_dict = {}
        for model in models:
            table_name = model._meta.db_table
            table_name = table_name.split('_')[1]
            attrs = [field.name for field in model._meta.fields]
            tables_dict[table_name] = attrs

        models_dict[_] = tables_dict

    return JsonResponse(models_dict)

@login_required
def enabled_methods(request):
    """
    This function was not implemented
    """

    if not request.user.is_staff:
        return JsonResponse({"error": "No puedes acceder a esta url"},status=403)

    apps_names = ["inventario", "compra", "usuario", "tarea", "herramienta"]

    models_dict = {}
    for _ in apps_names:
        app = apps.get_app_config(_)
        models = app.get_models()
        tables_dict = {}
        for model in models:
            table_name = model._meta.db_table
            table_name = table_name.split('_')[1]
            http_methods = [str(x) for x in inspect.getmembers(inv) if inspect.isclass(x[1])]
            tables_dict[table_name] = http_methods

        models_dict[_] = tables_dict

    return JsonResponse(models_dict)

@login_required
def enums_models(request):
    """
    Gets the scale (enums) in each attribute model
    
    :return: dict with the enums
    """


    def is_method(att):
        """
        Checks if the value returned by dir() corresponds to a method
        Note: the models defined in */models.py don't have their own methods"
        """

        return True if len(att) > 3 and att[-2:] == "__" and att[:2] == '__' else False

    def get_classes(dirs):
        return [name.lower() for name in dirs if not is_method(name)]

    def get_scales(scale_class):
        """
        Gets the scales (enums) in the given parameter class

        :param scale_class: the class that contains the enum
        :return: a list with the attribute's values
        """

        return [getattr((scale_class), att) for att in dir(scale_class) if not is_method(att) and att.isupper()]


    enums = {}
    tmp = {}
    tmp['unidadMedida'] = get_scales(inv.Insumo().MeasuresScale)
    #tmp['estado'] = get_scales(inv.Insumo().StatusScale)
    enums['insumos'] = tmp

    tmp = {}
    tmp['accionCantidad'] = get_scales(inv.ActionScale)
    enums['ajustes-stock'] = tmp

    tmp = {}
    tmp['estado'] = get_scales(her.StatusScale)
    enums['herramientas'] = tmp
    enums['estados-herramienta'] = tmp

    tmp = {}
    tmp['categoria'] = get_scales(tar.Empleado().CategoriaScale)
    enums['empleados'] = tmp

    tmp = {}
    tmp['prioridad'] = get_scales(tar.OrdenServicio().CaracterScale)
    tmp['categoria'] = get_scales(tar.OrdenServicio().CategoriaScale)
    tmp['estado'] = get_scales(tar.OrdenServicio().StatusScale)
    enums['ordenes-servicio'] = tmp

    tmp = {}
    tmp['satisfaccion'] = get_scales(tar.EncuestaSatisfaccion().SatisfactionScale)
    tmp['tiempoRespuesta'] = get_scales(tar.EncuestaSatisfaccion().ResponseTimeScale)
    enums['encuestasatisfaccion'] = tmp

    tmp = {}
    tmp['tipo'] = get_scales(tar.Tarea().TypeScale)
    tmp['clasificacion'] = get_scales(tar.Tarea().ClassificationScale)
    tmp['edificios'] = get_scales(tar.Sector().EdificioScale)
    enums['tareas'] = tmp

    tmp = {}
    tmp['responsable'] = get_scales(tar.Tiempo().CategoryScale)
    enums['tiempo'] = tmp

    tmp = {}
    tmp['aprobado'] = get_scales(com.StatusScale)
    enums['presupuestos'] = tmp

    aux = tmp['aprobado']
    tmp = {}
    tmp['recibido'] = aux
    enums['pedidos-insumo'] = tmp
    enums['detalle-pedidos'] = tmp

    tmp = {}
    tmp['edificio'] = get_scales(tar.Sector().EdificioScale)
    enums['sectores'] = tmp

    
    return JsonResponse(enums)
