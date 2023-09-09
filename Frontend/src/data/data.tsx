/**
 * Nombres en singular de modulos y en plural de tablas
 */
const names : Array<string> =[
    "inventario",
    "tipos-insumo",
    "insumos",
    "tipos-herramienta",
    "herramientas",
    "ordenes-retiro",
    "ajustes-stock",
    "estados-herramienta",
    "compra",
    "pedidos-insumo",
    "presupuesto",
    "detalle-pedidos",
    "usuario",
    "usuarios",
    "tarea",
    "empleados",
    "ordenes-servicio",
    "encuestas-satisfaccion",
    "tareas"
]

const translate ={
    [names[0]]:{singular:"Inventario",plural:"Inventarios"},
    [names[1]]:{singular:"Tipo de Insumo",plural:"Tipos de Insumo"},
    [names[2]]:{singular:"Insumo",plural:"Insumos"},
    [names[3]]:{singular:"Tipo de Herramienta",plural:"Tipos de Herramientas"},
    [names[4]]:{singular:"Herramienta",plural:"Herramientas"},
    [names[5]]:{singular:"Orden de Retiro",plural:"Ordenes de Retiro"},
    [names[6]]:{singular:"Ajuste de Stock",plural:"Ajustes de Stock"},
    [names[7]]:{singular:"Estado de Herramienta",plural:"Estados de Herramienta"},
    [names[8]]:{singular:"Compra",plural:"Compras"},
    [names[9]]:{singular:"Pedido de Insumo",plural:"Pedidos de Insumo"},
    [names[10]]:{singular:"Presupuesto",plural:"Presupuestos"},
    [names[11]]:{singular:"Detalle de Pedido",plural:"Detalles de Pedido"},
    [names[12]]:{singular:"Usuario",plural:"Usuarios"},
    [names[13]]:{singular:"Usuario",plural:"Usuarios"},
    [names[14]]:{singular:"Tarea",plural:"Tareas"},
    [names[15]]:{singular:"Empleado",plural:"Empleados"},
    [names[16]]:{singular:"Orden de Servicio",plural:"Ordenes de Servicio"},
    [names[17]]:{singular:"Encuesta de Satisfacción",plural:"Encuestas de Satisfacción"},
    [names[18]]:{singular:"Tarea",plural:"Tareas"},
}

/**
 * Objeto que contiene idexadas las caracterisitcas de las columnas de cada tabla
 * [
 * boolean(indica si se muestra en las tablas),
 * string(nombre de atributo),
 * string(nombre que se muestra),
 * string(tipo del dato),
 * float(porcentaje que indica para el tamaño de la columna)
 * ]
 */
export const tableColumnMetaData:Record<string,Record<string,Array<Array<any>>>> = {
    [names[0]]: {
        [names[1]]: [[true,"id","ID","number",0.05], [true,"nombre","Nombre","string",0.15], [false,"descripcion","Descripción","string",0.2]],
        [names[2]]: [[true,"id","ID","number",0.05], [true,"tipoInsumo","Tipo de Insumo","number",0.1],[true,"unidadMedida","Unidad de Medida","number",0.1],[true,"cantidad","Cantidad","number",0.1],[true,"codigo","Código","string",0.1], [false,"observaciones","Observaciones","string",0.1],[false,"puntoReposicion","Punto de Reposición","number",0.1]],
        [names[3]]: [[true,"id","ID","number",0.05], [true,"nombre","Nombre","string",0.15], [false,"descripcion","Descripción","string",0.2]], 
        [names[4]]: [[true,"id","ID","number",0.05], [true,"nombre","Nombre","string",0.15], [true,"tipoHerramienta","Tipo de Herramienta","number",0.05], [true,"codigo","Código","string",0.05], [true,"estado","Estado","string",0.15],[false,"fechaAlta","Fecha de Creación","string",0.15], [false,"observaciones","Observaciones","string",150]],
        [names[5]]: [[true,"id","ID","number",0.05], [true,"insumo","Insumo","number",0.05], [true,"tarea","Tarea","number",0.05], [true,"cantidad","Cantidad","number",0.05], [false,"fechaHora","Fecha","string",0.15]], 
        [names[6]]: [[true,"id","ID","number",0.05], [true,"insumo","Insumo","number",0.05], [true,"cantidad","Cantidad","number",0.05] ,[true,"observaciones","Observaciones","string",120], [false,"fecha","Fecha","string",0.15], "accionCantidad"], 
        [names[7]]: [[true,"id","ID","number",0.05], [true,"herramienta","Herramienta",0.05], [false,"fecha","Fecha","string",0.15], [false,"estado","Estado","string",0.15], [true,"observaciones","Observaciones","string",120]]
    },
    //falta completar lo demás
    [names[8]]: {
        [names[9]]: ["id", "fechaHora", "observaciones"],
        [names[10]]: ["id", "fecha", "proveedor", "total", "aprobado", "pedidoInsumo"],
        [names[11]]: ["id", "pedidoInsumo", "insumo", "cantidad", "observacion"]
    },
    [names[12]]: {
        [names[13]]: ["id", "legajo", "nombre", "apellido", "cargo", "mail", "telefono"]
    }, 
    [names[14]]: {
        [names[15]]: ["id", "dni", "nombre", "apellido", "telefono", "mail", "categoria"], 
        [names[16]]: ["id", "usuario", "tarea", "fechaGeneracion", "prioridad", "categoria", "estado"], 
        [names[17]]: ["id", "ordenServicio", "satisfaccion", "tiempoRespuesta", "observaciones"], 
        [names[18]]: ["id", "supTarea", "tipo", "descripcion", "fechaTentativa", "fechaInicio", "fechaFin"]
    }
}

function createModules(){
    return {
        id: 2,
        title: "Modulos",
        modules: 
        Object.keys(tableColumnMetaData).map((module,index)=>{
            return {
                id: index,
                title: translate[module].singular,
                url: `/${module}/`,
                icon: `/${module}.svg`,
                tables: Object.keys(tableColumnMetaData[module]).map((item,index)=>{
                    return {
                        id: index,
                        title: translate[item].singular,
                        url: `/${module}/${item}`,
                    }
                })
            }
        }),
    }
}

/**
 * 0-Principal,1-Modulos,2-Opciones,3-Analiticas;
 * Se utiliza para generar Routes,Sidebar y GetColumns.
 * Arreglo que contiene objetos que representan la estructura del modelo logico de la aplicacion
 * [Secciones{Modulos{Items}}]
 */
export const data = [
    {
        id: 1,
        title: "Principal",
        modules:[
            {
                id: 1,
                title: "Home",
                url: "/",
                icon: "/home.svg",
            },
            {
                id: 2,
                title: "Perfil",
                url: "/users/1",
                icon: "/user.svg",
            },
        ],
    },
    createModules(),
    {
        id: 4,
        title: "Opciones",
        modules: [
            {
                id: 1,
                title: "Opciones",
                url: "/",
                icon: "/setting.svg",
            },
            {
                id: 2,
                title: "Backups",
                url: "/",
                icon: "/backup.svg",
            },
        ],
    },
    {
        id: 5,
        title: "Analiticas",
        modules: [
            {
                id: 1,
                title: "Charts",
                url: "/",
                icon: "/chart.svg",
            },
            {
                id: 2,
                title: "Logs",
                url: "/",
                icon: "/log.svg",
            },
        ],
    },
];

function buildUrls(){
    const urls: Record<string,string> = {};
    Object.keys(tableColumnMetaData).forEach((module)=>{
        Object.keys(tableColumnMetaData[module]).forEach((item)=>{
            urls[item]=`/${module}/${item}`;
        })
    })
    return urls;
}

export const backendUrls: Record<string,string>=buildUrls()