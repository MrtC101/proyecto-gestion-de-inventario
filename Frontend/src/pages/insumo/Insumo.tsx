import "./insumo.scss"
import Single from "../../components/single/Single"
import { singleItem } from "../../data"
import { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
const Insumo = () => {

  // Fetch data and send to Single Component
    const [insumo, setInsumo] = useState([]);
    const { id } = useParams()
    useEffect(() => {
        
        axios.get(`http://127.0.0.1:8000/inventario/insumos/${id}`)
        .then((response) => {
            setInsumo(response.data);

        })
        .catch((error) => {
            console.error("Error al obtener datos de /inventario/insumos");
        });
    }, []);
    

    return (
        <div className="item">
        <Single {...singleItem} />
        </div>
    )

}

export default Insumo
