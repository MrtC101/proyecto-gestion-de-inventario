import "./serviceform.scss"
import { Form, FormGroup } from "react-bootstrap";
import { createContext, useContext, useEffect, useState, useRef } from "react";

import { GetEnums, SendServiceRequest } from "../../../../Api/apiService";

import { setMessage } from "../../../providerComponents/messageDisplay/MessageDisplay";

import { getSectors } from "../../../../Api/apiService";
import { useAuthData } from "../../../providerComponents/authProvider/AuthProvider";

export default function ServiceForm(){

    const formRef  = useRef();
    const edificioSelect = useRef();
    const sectorSelect = useRef();
    
    const [authData] = useAuthData();

    ///Select de Edificios
        const [enums, setEnum] = useState("");
        useEffect(() => {
            const fetchData = async () => {
                await GetEnums(setEnum); 
            };
            fetchData();
        }, []);

        const [currOption,setCurrOption] =  useState("");    
        useState(()=>{setCurrOption("")},[enums]);
        const changeHandler = e => {
            changeID();
            setCurrOption(e.target.value)};
    ///

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        // Prevent the browser from reloading the page
        e.preventDefault();
        const form = e.currentTarget as HTMLFormElement;
        const formData = new FormData(form);
        formData.append("usuario",authData["id"].toString())
        console.log(formData)
        SendServiceRequest(formData)
        .then(() => {
            try{
                formRef.current.reset()
                setMessage(`Se ha enviado el formulario con éxito`,null)
            }catch(e){
                setMessage(`Error al reiniciar el Formulario`,e)
            }
        })
        .catch((error) => {
            setMessage(`Ha surgido un error al enviar el formulario`,error)
        })
    };

    //BLOCK
    const [sectors,setSectors] = useState([]);
    const [edificioname,setEdificioID] = useState(null);

    useEffect(()=>{
        if(edificioname !== null){
            getSectors(setSectors,edificioname)
            .catch((error) => {
                setMessage(`No se pudo conectar con el servidor`,error)
            })
        }
    },[edificioname])

    //console.log(sectors)
    //console.log(edificioname)
    //endBLOCK

    const changeID = () => {
        if(sectorSelect.current!.value !== ""){
            sectorSelect.current.value = "";
        }
        setEdificioID(edificioSelect.current.value);
    }

    //console.log(sectors)
    return (
        <>
        <div className="serviceForm">           

            <div className="container">
                
                <h1>Generar Solicitud de Mantenimiento</h1>
                <h5>Formulario para describir las necesidades de mantenimiento detectadas/relevadas por personal de la FI </h5>
                
                <div className="comm-info">Cualquier duda comunicarse al  4135000 interno 2137 o al 2615068289</div>
                
                <form ref={formRef} method="post" onSubmit={handleSubmit}>
                    
                    <div className="form-group">
                    <label>Sector de la necesidad</label>
                        <div className="two-fields">                           
                            <Form.Select
                                ref={edificioSelect}
                                className="form-select mx-1"
                                value={currOption}
                                required={true}
                                onChange={changeHandler}
                            >
                                <option value="" disabled>Elegir {"edificio"}</option>
                                {enums!==""?
                                enums["sectores"]["edificio"].map(unidad => (
                                    <option value={unidad} key={unidad}>{unidad}</option>
                                ))
                                :null}
                            </Form.Select>
                            
                            <select required ref={sectorSelect} className="form-select mx-1" name="sector" defaultValue={""}>
                                <option value="" defaultValue={""} disabled>Selecciona un Sector</option>
                                {sectors.map((obj)=><option key={obj.id} value={obj.id}>{obj.nombre}</option>)}
                            </select>
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Descripción de la necesidad de mantenimiento/reparación</label>
                        <textarea required className="form-control" name="descripcion" maxLength={120} />
                    </div>

                    <div className="form-group">
                        <label>Detalle de la necesidad de mantenimiento/reparación</label>
                        <select required name="categoria" className="form-select" defaultValue={""}>
                            <option value="" disabled>Selecciona un tipo</option>
                            <option value="FABRICACION">Fabricación</option>
                            <option value="TRASLADOS">Movimiento de materiales / traslados</option>
                            <option value="MODIF/ADEC">Modificación/adecuación</option>
                        </select>
                    </div>
                    
                    <div className="form-group">
                        <label>Carácter de la necesidad</label>
                        <select required name="prioridad" className="form-select" defaultValue={""}>
                            <option value="" disabled>Selecciona el carácter</option>
                            <option value="NORMAL">Normal (sin urgencia)</option>
                            <option value="URGENTE">Urgente</option>
                            <option value="CRITICO">Crítica</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label>Fecha de Necesidad (cuando debe estar resuelta la necesidad)</label>
                        <input required className="form-control" type="date" name="fechaNecesidad" maxLength={120}/>
                    </div>
                    <div className="form-group">
                        <label>Añadir algún comentario</label>
                        <textarea className="form-control" name="comentario" maxLength={120}/>
                    </div>

                    <button className="btn btn-primary" type="submit">Enviar</button>
                </form>
            </div>
        </div>
        <div className="footer">
            <span>UNCUYO - Facultad de Ingeniería</span>
            <img src="/images/Institution_Logo.jpeg"/>
        </div>
        </>
    )
}