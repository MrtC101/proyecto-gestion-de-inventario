import { RouteObject, RouterProps, createBrowserRouter,redirect} from "react-router-dom";

import Home from "./pages/HomePage";
import About from "./pages/AboutPage";
import Dashboard from "./pages/DashboardPage";
import ErrorPage from "./pages/ErrorPage"

import ItemList  from "./components/List/List";
import {CreateForm,ReadForm,UpdateForm,DeleteForm} from "./components/Form/Form";
import {ReadItem,FormSubmitter} from "./components/Api/apiService";
import { resources } from "./components/Api/apiService";

/**
 * Variable que contiene las rutas que se renderizarán.
 * Algunas consideraciones:
 * Capos de un objeto tipo ruta en este formato de declaración:
 * interface RouteObject {
      path?: string;
      index?: boolean;
      children?: React.ReactNode;
      caseSensitive?: boolean;
      id?: string;
      loader?: LoaderFresourcesunction;
      action?: ActionFunction;
      element?: React.ReactNode | null;
      Component?: React.ComponentType | null;
      errorElement?: React.ReactNode | null;
      ErrorBoundary?: React.ComponentType | null;
      handle?: RouteObject["handle"];
      shouldRevalidate?: ShouldRevalidateFunction;
      lazy?: LazyRouteFunction<RouteObject>;
  }
  (IMPORTANTE QUE RESPETE EL NOMBRE que es caseSensitive)
  informacion: https://reactrouter.com/en/main/route/route
  (loader:es una funcion que se ejecuta antes de cargar la vista)
  (handler: es una funcion que se ejecuta una vez cargada la pagina)
  (las rutas index,layout y el outlet son conceptos importantes)
 */


function getItemRoutes(){
  var routes:any[] = [];
  Object.keys(resources).forEach((module) => {
    Object.keys(resources[module]).forEach((item) => {
        const newRoutes = [
        {
          path:`${module}/${item}`,
          element: <ItemList/>,
          errorElement:ErrorPage
        },
        {
          path: `${module}/${item}/create/`,
          element: <CreateForm/>,
          action: FormSubmitter
        },
        {
          path: `${module}/${item}/read/:id`,
          element: <ReadForm/>,
          action: ReadItem
        },
        {
          path: `${module}/${item}/update/:id`,
          element: <UpdateForm/>,
          action: FormSubmitter
        },
        {
          path: `${module}/${item}/delete/:id`,
          element: <DeleteForm/>,
          action: FormSubmitter
        }];
        routes = routes.concat(newRoutes)
      return ;});
    return ;});
    routes.push(
      {
        index:true,
        element: <Home/>
      }
    );
    return routes;
  }
/**
 * Array que contiene los objetos que definen las rutas de la aplicación
 */

var routes :RouteObject[] = [
  {
    path: "/",
    loader: () => (redirect("/home"))
  },
  {
    path: "/home",
    loader: () => ( redirect("/Dashboard")),
    element: <Home/>,
    children: [
      {
        index:true,
        path:"/home/about",
        element: <About/>
      }
    ]
  },
  {
    path: "/Dashboard/",
    element: <Dashboard/> ,
    children : getItemRoutes()
  }
];

const router = createBrowserRouter(routes);
export default router;