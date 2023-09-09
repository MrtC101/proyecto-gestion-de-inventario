import "./delete.scss"
import { DeleteItem} from "../../Api/apiService"; 
import { ReadItem,GetUrlParts } from "../../Api/apiService";
import {useState} from "react";
import { Link, useParams } from "react-router-dom";

const Delete = () => {
    const [row, setRow] = useState(null);
    const {item:itemName,module:moduleName} = GetUrlParts();
    const id = useParams().id;
    ReadItem(setRow,itemName);

    const handleDelete = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        DeleteItem(itemName,id);
    };

    var r = <div>
        <h1>El {itemName} con id {id} no existe o ha sido borrado anteriormente.</h1>
    </div>
    if(row){
        r= <div className="addItem">
            <div className="modal">
                <h1>Eliminar {itemName}</h1>
                <h2>¿Está usted seguro de que quiere eliminar el {itemName} con identificador {id}?</h2>
                <form method="post" onSubmit={handleDelete}>
                    <button type="submit">Eliminar</button>
                </form>
                <Link to={`/${moduleName}/${itemName}`} >
                    <button className="button">Atras</button>
                </Link>
            </div>
        </div>
    }
    return (r);
};

export default Delete;