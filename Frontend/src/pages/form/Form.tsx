import "./form.scss"
import {GetUrlParts,UpdateItem as Update,ReadItem as Read} from "../../Api/apiService"
import { useState } from "react";
import { Link, useParams } from "react-router-dom";

function Form(){
    const [row, setRow] = useState([]);
    const {item:itemName,module:moduleName} = GetUrlParts();
    const {id} = useParams();

    Read(setRow,itemName);

    interface formDataType { [key: string]: FormDataEntryValue }
    
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        // Prevent the browser from reloading the page
        e.preventDefault();
        const form = e.currentTarget as HTMLFormElement;
        const formData = new FormData(form);
        
        Update(itemName,formData,id);
    };

    return (
        <div>
            <div className="modal">
                <h1>Modificar {itemName}</h1>
                <form method="post" onSubmit={handleSubmit}>
                    {Object.keys(row).map((key,index) => (
                            <div className="item" key={index}>
                                <label htmlFor="1">{key}</label>
                                <input
                                    type="string"
                                    name={key}
                                    //placeholder={key}
                                    defaultValue={row[key]}
                                    />
                            </div>
                        ))}
                    <button type="submit">Modificar</button>
                </form>
                <Link to={`/${moduleName}/${itemName}`} >
                      <button className="button">Atras</button>
                </Link>
            </div>
        </div>
    );
}

export default Form; 