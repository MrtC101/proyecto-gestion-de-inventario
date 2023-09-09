import { RouteObject, createBrowserRouter, redirect } from "react-router-dom";


import Dashboard from "../pages/dashboard/Dashboard";
import Login from "../pages/login/Login";
import Home from "../pages/home/Home";

/*información: https://reactrouter.com/en/main/route/route*/


import Detail from "../pages/detail/Detail"
import List from "../pages/list/List"
import Form from "../pages/form/Form"
import Delete from "../pages/delete/Delete"
//import Resume
import {data as sideBarContent} from "../data/data.tsx";

/**
 * Genera a partir de los elementos del menu lateral las url's correspondientes
 * @returns Un arreglo con todas las rutas para inventario
 */
function getRoutes(){
  var routes :RouteObject[] = [];
  sideBarContent.forEach((section) => {
    section.modules.forEach((module) => {
        routes.push(
          {
            path:module.url,
            loader: () => {return redirect(module.tables[0].url)}
          }
        );
        module.tables?.forEach((item)=>{
          routes = routes.concat([
            {
              path: item.url,
              element: <List/>,
            },
            {
              path: item.url+"/detail/:id/",
              element: <Detail/>
            },
            {
              path: item.url+"/modify/:id/",
              element: <Form/>,
            },
            {
              path: item.url+"/delete/:id/",
              element: <Delete/>,
            }
          ]);
        })
      });
    });
    
    return routes;
  }
  


/**
 * Arreglo que contiene todas lasconst backendUrls: Record<string,string>  ={
    "insumos":"/inventario/insumos",
    "tipos-insumo":"/inventario/tiposInsumo",
    "Herramientas":"/inventario/herramienta",
    "Tipo De Herramienta":"/inventario/tipoHerramienta",
} rutas de la aplicación
 */
var routes = [
  {
    path: "/",
    element: <Dashboard />,
    children: getRoutes().concat(
    [
      {
        index:true,
        path: "/",
        element: <Home />
      }
    ])
  },
  {
    path: "/login",
    element: <Login />
  }
];

const router = createBrowserRouter(routes);
export default router;