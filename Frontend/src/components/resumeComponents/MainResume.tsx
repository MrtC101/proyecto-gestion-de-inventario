
import "./mainResume.scss"

import TopPendingTasks from "./topPendingTasks/TopPendingTasks"
import TopPendingReposition from "./topPendingReposition/TopPendingReposition"
import PieConsumed from "./pieConsumed/PieConsumed";
import TaskCompletedChart from "./taskCompletedChart/taskCompletedChart";
import HoursChart from "./hoursChart/hoursChart";

function MainResume() {

  //Tareas pendientes (Primeras 10)
  //Stock bajo del punto de reposición (Primero 10)  
  //Productos-más consumidos por tareas en general (Grafico Torta, 5)
  //Cantidad de Ajustes de stock realizadas por mes este año(Historico)
  //Cantidad de tareas completadas por més este año (Historico)
  
  return (
    <div className="home">
      <div className="box box1"><TopPendingTasks/></div> 
      <div className="box box7"><PieConsumed/></div>
      <div className="box box1"><TopPendingReposition/></div>
    </div>
  )
}

//<div className="box box2"><HoursChart/></div>
//<div className="box box3"><TaskCompletedChart/></div>
      
export default MainResume;
