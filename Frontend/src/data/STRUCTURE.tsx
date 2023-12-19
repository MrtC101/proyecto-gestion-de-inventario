enum SIZE {
    ID = 25,
    VERYTINY = 50,
    TINY = 100,
    SMALL = 150,
    MEDIUM = 250,
    BIG = 350,
}
/**
 * Constante que depende del MER del back-end y refleja:
 * - grupos de entidades
 * - atributos de cada entidad
 * - meta-atributos de cada atributo (relacionados con las columnas de las tablas)
 * La estructura es:
 * "grupo":{
 *      "entidad":{
 *          "atributo":{
 *             meta_atributo;
 *          }
 *      }
 * }
 * Depende de el nombre de las entidades, y el nombre de los atributos del MER.
 */
const STRUCTURE: Record<string, Record<string, Record<string, Record<string, any>>>> = {
    "inventario": {
        "insumos": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "nombre": {
                editable: true,
                show: true,
                name: "Nombre",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "tipoInsumo": {
                editable: true,
                show: true,
                name: "Tipo de Insumo",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: false
            },
            "unidadMedida": {
                editable: true,
                show: true,
                name: "Unidad de Medida",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: true
            },
            "cantidad": {
                editable: true,
                show: true,
                name: "Cantidad",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "codigo": {
                editable: true,
                show: true,
                name: "Código",
                type: "string",
                col_size: SIZE.TINY,
                required: false,
                select: false,
                enum: false
            },
            "observaciones": {
                editable: true,
                show: false,
                name: "Observaciones",
                type: "string",
                col_size: SIZE.SMALL,
                required: false,
                select: false,
                enum: false
            },
            "puntoReposicion": {
                editable: true,
                show: true,
                name: "Punto de Reposición",
                type: "number",
                col_size: SIZE.TINY,
                required: false,
                select: false,
                enum: false
            },
            "baja": {
                editable: false,
                show: false,
                name: "Dado de Baja",
                type: "string",
                col_size: SIZE.TINY,
                required: false,
                select: false,
                enum: false,
            }

        },
        "tipos-insumo": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false,
            },
            "nombre": {
                editable: true,
                show: true,
                name: "Nombre",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "descripcion": {
                editable: true,
                show: true,
                name: "Descripción",
                type: "string",
                col_size: SIZE.BIG,
                required: false,
                select: false,
                enum: false
            }
        },
        "ordenes-retiro": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "insumo": {
                editable: true,
                show: true,
                name: "Insumo",
                type: "number",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: false
            },
            "tarea": {
                editable: true,
                show: true,
                name: "Tarea",
                type: "number",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: false
            },
            "cantidad": {
                editable: true,
                show: true,
                name: "Cantidad",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "fechaHora": {
                editable: false,
                show: false,
                name: "Fecha",
                type: "date",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
        },
        "ajustes-stock": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "insumo": {
                editable: true,
                show: true,
                name: "Insumo",
                type: "number",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: false
            },
            "cantidad": {
                editable: true,
                show: true,
                name: "Valor",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "accionCantidad": {
                editable: false,
                show: true,
                name: "Accion",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "observaciones": {
                editable: true,
                show: true,
                name: "Observaciones",
                type: "string",
                col_size: SIZE.BIG,
                required: true,
                select: false,
                enum: false
            },
            "fecha": {
                editable: false,
                show: true,
                name: "Fecha",
                type: "date",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
        },
        "herramientas": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "nombre": {
                editable: true,
                show: true,
                name: "Nombre",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "tipoHerramienta": {
                editable: true,
                show: true,
                name: "Tipo de Herramienta",
                type: "number",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: false
            },
            "codigo": {
                editable: true,
                show: true,
                name: "Código",
                type: "string",
                col_size: SIZE.TINY,
                required: false,
                select: false,
                enum: false
            },
            "estado": {
                editable: true,
                show: true,
                name: "Estado",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: true
            },
            "fechaAlta": {
                editable: false,
                show: true,
                name: "Fecha de Creación",
                type: "date",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "observaciones": {
                editable: true,
                show: true,
                name: "Observaciones",
                type: "string",
                col_size: SIZE.BIG,
                required: false,
                select: false,
                enum: false
            },
        },
        "tipos-herramienta": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "nombre": {
                editable: true,
                show: true,
                name: "Nombre",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "descripcion": {
                editable: true,
                show: true,
                name: "Descripción",
                type: "string",
                col_size: SIZE.BIG,
                required: false,
                select: false,
                enum: false
            },
        },
        "estados-herramienta": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "herramienta": {
                editable: false,
                show: true,
                name: "Herramienta",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: false
            },
            "estado": {
                editable: false,
                show: true,
                name: "Estado",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: true,
                enum: true
            },
            "fecha": {
                editable: false,
                show: true,
                name: "Fecha",
                type: "date",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "observaciones": {
                editable: false,
                show: true,
                name: "Observaciones",
                type: "string",
                col_size: SIZE.SMALL,
                required: false,
                select: false,
                enum: false
            },
        }
    },
    "compra": {
        "pedidos-insumo": {
            "id": {
                editable: false,
                show: true,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "fechaHora": {
                editable: false,
                show: true,
                name: "Fecha de creación",
                type: "date",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "observaciones": {
                editable: true,
                show: true,
                name: "Observacion",
                type: "string",
                col_size: SIZE.BIG,
                required: false,
                select : false,
                enum: false
            },
            "recibido": {
                editable: true,
                show: true,
                name: "Recibido",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select : true,
                enum: true
            },
        },
        "detalle-pedidos": {
            "id": {
                editable: false,
                show: true,
                name: "ID",
                type: "number",
                col_size: SIZE.ID,
                required: true,
                select : false,
                enum: false
            },
            "pedidoInsumo": {
                editable: true,
                show: true,
                name: "Pedido de Insumo",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select : true,
                enum: false
            },
            "insumo": {
                editable: true,
                show: true,
                name: "Insumo pedido",
                type: "number",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: false
            },
            "cantidad": {
                editable: true,
                show: true,
                name: "Cantidad",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "observacion": {
                editable: true,
                show: false,
                name: "Observacion",
                type: "string",
                col_size: SIZE.BIG,
                required: false,
                select: false,
                enum: false
            },
        },
        "presupuestos": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "pedidoInsumo": {
                editable: true,
                show: true,
                name: "Pedido de Insumo",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: true,
                enum: false
            },
            "fecha": {
                editable: true,
                show: true,
                name: "Fechas",
                type: "date",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "proveedor": {
                editable: true,
                show: true,
                name: "Proveedor",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "total": {
                editable: true,
                show: true,
                name: "Total",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "aprobado": {
                editable: true,
                show: true,
                name: "Aprobado",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: true
            },
        }
    },
    "usuario": {
        "usuarios": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "username": {
                editable: true,
                show: true,
                name: "Nombre de usuario",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "password": {
                editable: true,
                show: false,
                name: "Contraseña",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "first_name": {
                editable: true,
                show: true,
                name: "Nombre",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "last_name": {
                editable: true,
                show: true,
                name: "Apellido",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "email": {
                editable: true,
                show: true,
                name: "Dirección de Correo Electrónico",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: false,
            },
            "is_staff": {
                editable: true,
                show: true,
                name: "Es Administrador",
                type: "checkbox",
                col_size: SIZE.TINY,
                required: false,
                select: false,
            },
            "date_joined": {
                editable: false,
                show: true,
                name: "Fecha de Creación",
                type: "date",
                col_size: SIZE.TINY,
                required: false,
                select: false,
            },
            "legajo": {
                editable: true,
                show: true,
                name: "Legajo",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "cargo": {
                editable: true,
                show: true,
                name: "Cargo",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "telefono": {
                editable: true,
                show: true,
                name: "Teléfono",
                type: "phone",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
        }
    },
    "tarea": {
        "tareas": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "ordenServicio": {
                editable: false,
                show: true,
                name: "Nº Orden",
                type: "number",
                col_size: 80,
                required: true,
                select: false,
                enum: false
            },
            "descripcion": {
                editable: true,
                show: true,
                name: "Descripción",
                type: "string",
                col_size: SIZE.BIG,
                required: true,
                select: false,
                enum: false
            },
            "clasificacion":{
                editable: true,
                show: true,
                name: "Clasificación",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: true,
                enum: true
            },
            "tipo": {
                editable: true,
                show: true,
                name: "Tipo",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: true,
                enum: true
            },
            
            "empleados": {
                editable: true,
                show: false,
                name: "Empleados",
                type: "string",
                col_size: SIZE.SMALL,
                required: false,
                select: false,
                enum: false

            },
            "herramientas": {
                editable: true,
                show: false,
                name: "Herramientas",
                type: "string",
                col_size: SIZE.SMALL,
                required: false,
                select: false,
                enum: false
            },
            "retiros_insumos": {
                editable: true,
                show: false,
                name: "Insumo",
                type: "string",
                col_size: SIZE.SMALL,
                required: false,
                select: false,
                enum: false
            },
            "fechaTentativa": {
                editable: true,
                show: true,
                name: "Fecha tentantiva",
                type: "date",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "fechaInicio": {
                editable: true,
                show: true,
                name: "Fecha de Inicio",
                type: "date",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "fechaFin": {
                editable: true,
                show: true,
                name: "Fecha de Finalizacion",
                type: "date",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "userAuth": {
                editable: false,
                show: false,
                name: "userAuth",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
        },
        "empleados": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "dni": {
                editable: true,
                show: true,
                name: "DNI",
                type: "number",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "nombre": {
                editable: true,
                show: true,
                name: "Nombre",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "apellido": {
                editable: true,
                show: true,
                name: "Apellido",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "telefono": {
                editable: true,
                show: true,
                name: "Teléfono",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "mail": {
                editable: true,
                show: true,
                name: "Mail",
                type: "email",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "categoria": {
                editable: true,
                show: true,
                name: "Categoría",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: true,
                enum: true
            },
            
        },
        "ordenes-servicio": {
            "id": {
                editable: false,
                show: true,
                name: "ID",
                type: "number",
                col_size: SIZE.ID,
                required: true,
                select: false,
                enum: false
            },
            "usuario": {
                editable: true,
                show: false,
                name: "Usuario",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: true,
                enum: false
            },
            //Estos se han agregado ya que recibimos los datos dle usuario desde el back
            "usuarioID": {
                editable: false,
                show: false,
                name: "ID de usuario",
                type: "string",
                col_size: SIZE.TINY,
                required: false,
                select: false,
                enum: false
            },
            "usuarioNombre": {
                editable: false,
                show: true,
                name: "Usuario",
                type: "string",
                col_size: SIZE.TINY,
                required: false,
                select: false,
                enum: false
            },
            "usuarioApellido": {
                editable: false,
                show: true,
                name: "Apellido",
                type: "string",
                col_size: SIZE.TINY,
                required: false,
                select: false,
                enum: false
            },
            
            "fechaGeneracion": {
                editable: false,
                show: true,
                name: "Fecha de Generación",
                type: "date",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
            "sector": {
                editable: true,
                show: false,
                name: "Sector",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                enum: false
            },
            "descripcion": {
                editable: true,
                show: false,
                name: "Descripción",
                type: "string",
                col_size: SIZE.SMALL,
                required: false,
                enum: false
            },
            "categoria": {
                editable: true,
                show: true,
                name: "Categoría",
                type: "number",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: true
            },
            "prioridad": {
                editable: false,
                show: true,
                name: "Prioridad",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: true,
                enum: true
            },
            "fechaNecesidad": {
                editable: true,
                show: true,
                name: "Fecha de Necesidad",
                type: "date",
                col_size: SIZE.SMALL,
                required: false,
                select: false,
                enum: false
            },
            "comentario": {
                editable: true,
                show: false,
                name: "Comentario",
                type: "string",
                col_size: SIZE.SMALL,
                required: false,
                enum: false
            },
            "estado": {
                editable: true,
                show: true,
                name: "Estado",
                type: "number",
                col_size: SIZE.SMALL,
                required: true,
                select: true,
                enum: true
            },
        },
        "sectores": {
            "id": {
                editable: false,
                show: false,
                name: "ID",
                type: "number",
                col_size: SIZE.TINY,
                required: true,
                select: false,
                enum: false
            },
            "edificio": {
                editable: true,
                show: true,
                name: "Edificio",
                type: "string",
                col_size: SIZE.TINY,
                required: true,
                select: true,
                enum: true
            },
            "nombre": {
                editable: true,
                show: true,
                name: "Sector",
                type: "string",
                col_size: SIZE.SMALL,
                required: true,
                select: false,
                enum: false
            },
        }
    },
}

export default STRUCTURE;

//================GETTERS Y FUNCIONES================//

/**
 * (getter) getFullName: devuelve el meta-atributo name de STRUCTURE
 * @param group Nombre del grupo de la estructura
 * @param entity Nombre de la entidad
 * @param attribute Nombre del atributo
 * @returns Devuelve el valor que se encuentra en el meta-atributo name de un atributo.
 */
export function getFullName(group: string, entity: string, attribute: string): string | undefined {
    try {
        return STRUCTURE[group][entity][attribute]["name"];
    } catch {
        throw new Error(`No se encuentra el atributo 
        ${group}->${entity}->${attribute}`)
    }
}

import { GridColDef } from "@mui/x-data-grid";
/**
 * (getter + function) GetColumns: devuelve un arreglo con objetos
 * que contiene atributos de las columnas de la tabla los cuales están en función
 * de los meta-atributos de los atributos de cada entidad definida
 * en la variable STRUCTURE.
 * @param group nombre grupo al que pertenece la entidad
 * @param entity nombre de la entidad
 * @returns 
 */
export function GetColumns(group: string, entity: String): GridColDef[] {
    //console.log(group,entity)
    return Object.entries(STRUCTURE[group][entity])
        .filter(([key, attribute]) => attribute.show === true)
        .map(([key, attribute]) => {

            var getter = attribute.type === "date" ?
                (params) => { return new Date(params.value) } : null

            return {
                field: key,
                headerName: attribute.name,
                type: attribute.type,
                width: attribute.col_size,
                valueGetter: getter
            };
        });
}

export type Field = {
    field: string,
    headerName: string,
    type: string,
    required: boolean,
    editable: boolean,
    select: boolean,
    enum: boolean;
}

export function GetFields(group: string, entity: String): Field[] {
    return Object.entries(STRUCTURE[group][entity])
        .map(([key, attribute]) => {
            return {
                field: key,
                headerName: attribute.name,
                type: attribute.type,
                required: attribute.required,
                editable: attribute.editable,
                select: attribute.select,
                enum: attribute.enum
            };
        });
}