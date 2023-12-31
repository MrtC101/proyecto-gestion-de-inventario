import STRUCTURE from "./STRUCTURE"
 
/**
 * IP y puerto del backend.
 */
export const BASEURL = "http://127.0.0.1:8000"

/**
* Construye las url's del backend, en función de la los grupos lógicos
* y las entidades que se reflejan en la variable STRUCTURE.
* @returns Diccionario<entidad,url>
*/
function buildURLs(){
    const urls: Record<string, string> = {};
    Object.keys(STRUCTURE).forEach((module) => {
        Object.keys(STRUCTURE[module]).forEach((entity) => {
            urls[entity] = `/${module}/${entity}/`
        })
    })
    urls["enums"] = "/table-enums/";
    urls["edificios"] = "tarea/sector/edificios/";
    urls["presupuestos-filtered"] = "compra/pedidos-insumo/presupuestos/";
    urls["detalle-pedidos-filtered"] = "compra/pedidos-insumo/detalles/";    
    urls["stat-reposition"] = "stats/insumos-bajo-reposicion/";
    urls["stat-tasks"] = "stats/tareas-pendientes-urgentes/";
    urls["stat-consumed"] = 'stats/insumos-mas-consumidos/';
    urls["stat-completed"] = 'stats/tareas-completadas/';
    urls["stat-hours"] = 'stats/empleados-horas-totales/';
    return urls;
}
/**
 * Endpoints(URL's) del backend utilizados por apiService.tsx
 * Depende de los grupos, y las entidades del MER definidas en STRUCTURE.
 */
const BACKENDURLS: Record<string, string> = buildURLs();

export function getBackendUrl(name){
    try{
        return BACKENDURLS[name];
    }catch{
        throw new Error(`No existe url en el backend para ${name}`);
    }
}