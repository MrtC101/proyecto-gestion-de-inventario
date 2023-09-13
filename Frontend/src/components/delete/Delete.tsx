import "./delete.scss"
import {DeleteItem} from "../../Api/apiService"; 
import {ReadItem,GetUrlParts } from "../../Api/apiService";
import {useState, useContext} from "react";
import {Link, useParams} from "react-router-dom";
import {crudContext, getSingular} from "../../data/data";

const Delete = () => {
    const [row, setRow] = useState(null);
    const {item:itemName,module:moduleName} = GetUrlParts();
    const id = useParams().id;

    const [msg,setMsg] = useContext(crudContext)

    ReadItem(setRow,itemName);

    const handleDelete = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try{
            DeleteItem(itemName,id);
            setMsg([`Se ha eliminado el ${getSingular(itemName)} ${id} con exito`, false])
        }catch(error){
            setMsg([`Ha surgido un error al eliminar el ${getSingular(itemName)} ${id}`, true])
        }finally{
            history.back();
        } 
    };

    var r = <div>
        <h1>El {getSingular(itemName)} con id {id} no existe o ha sido borrado anteriormente.</h1>
    </div>
    if(row){
        r= <div className="delete">
            <div className="modal2">
                <h1>Eliminar {getSingular(itemName)}</h1>
                <h2>¿Está usted seguro de que quiere eliminar el {getSingular(itemName)} con identificador {id}?</h2>
                <form method="post" onSubmit={handleDelete}>
                    <button className="btn btn-danger" type="submit">Eliminar</button>
                </form>
                <Link to={`/${moduleName}/${itemName}`} >
                    <button className="btn btn-secondary">Atras</button>
                </Link>
            </div>
        </div>
    }
    return (r);
};

export default Delete;