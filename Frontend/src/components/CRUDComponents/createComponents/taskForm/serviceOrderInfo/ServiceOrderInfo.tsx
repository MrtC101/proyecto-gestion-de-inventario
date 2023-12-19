import "./serviceOrderInfo.scss"
import { Button, Col, Row } from 'react-bootstrap'
import Form from 'react-bootstrap/Form';
import "./serviceOrderInfo.scss"
import { UpdateItem } from "../../../../../Api/apiService";
import { useEffect, useState } from "react";
import { setMessage } from "../../../../providerComponents/messageDisplay/MessageDisplay";


interface ServiceOrder {
    id: number | string,
    estado: string,
    usuarioNombre: string,
    usuarioApellido: string,
    sector: string,
    categoria: string,
    descripcion: string,
    prioridad: string,
    fechaNecesidad: string,
    comentario: string | null,
    [key: string]: any;

}

interface Props {
    serviceOrder: ServiceOrder,
    action: "update" | "create"
}


export const ServiceOrderInfo = (props:Props) => {
    /**
     * Cambia el estado de la orden de servicio 
     */
    const [status, setStatus] = useState(props.serviceOrder["estado"]);


    useEffect(() => {

    }, [status]);

    const changeStatus = () => {
        var newStatus: string = status;

        if (status === "EN_ESPERA" || status === "APROBADA") {
            newStatus = "RECHAZADA";
            setStatus("RECHAZADA");
        }
        if (status === "RECHAZADA") {
            newStatus = "APROBADA"
        }
        setStatus(newStatus);
    
        const formData = new FormData();
        // Agregar propiedades del serviceOrder a FormData  
        formData.append("categoria", props.serviceOrder["categoria"]);
        if (props.serviceOrder["comentario"] !== null) formData.append("comentario", props.serviceOrder["comentario"]);
        formData.append("descripcion", props.serviceOrder["descripcion"]);
        formData.append("estado", newStatus);
        formData.append("fechaGeneracion", props.serviceOrder["fechaGeneracion"]);
        formData.append("fechaNecesidad", props.serviceOrder["fechaNecesidad"]);
        formData.append("prioridad", props.serviceOrder["prioridad"]);
        formData.append("sector", props.serviceOrder["sectorID"]);
        formData.append("usuario", props.serviceOrder["usuarioID"]);

        UpdateItem("ordenes-servicio", formData, props.serviceOrder["id"].toString())
            .then((response) => { console.log(response); window.location.reload(); })
            .catch((error) => { setMessage("Se produjo un error al cambiar el estado de la Orden de servicio.", error) });
        
    }

    return (
            <Col xs={5} className="service-order">
                <div className="row">
                    <h4 className="col">Orden de servicio</h4>
                    
                    {props.serviceOrder["estado"] === "FINALIZADA" &&
                        <div className="col status rounded p-2 bg-success m-1">{props.serviceOrder["estado"]}</div>}
                    {props.serviceOrder["estado"] === "EN_ESPERA" &&
                        <div className="col status rounded p-2 bg-secondary m-1">EN ESPERA</div>}
                    {props.serviceOrder["estado"] === "RECHAZADA" &&
                        <div className="col status rounded p-2 bg-danger m-1">RECHAZADA</div>}
                    {props.serviceOrder["estado"] === "APROBADA" &&
                        <div className="col status rounded p-2 bg-light text-dark m-1">APROBADA</div>}
                    {props.serviceOrder["estado"] === "EN_PROGRESO" &&
                        <div className="col status rounded p-2 bg-light text-dark m-1">EN PROGRESO</div>}

                    
                        
                                 
                    
                    {props.action === "create" && (status === "EN_ESPERA" || status === "APROBADA") && (
                        <Button className="btn btn-danger m-1 p-2 col" onClick={changeStatus}>
                            Rechazar
                        </Button>
                    )}
                    {props.action === "create" && status === "RECHAZADA" && (
                        <Button className="btn btn-success m-1 p-2 col" onClick={changeStatus}>
                            Aprobar
                        </Button>
                    )}
                </div>
                
                <Row className="mb-3">
                    <Form.Group as={Col} controlId="no">
                        <Form.Label>Nombre</Form.Label>
                        <Form.Control disabled type="string" value={props.serviceOrder["usuarioNombre"]} />
                    </Form.Group>

                    <Form.Group as={Col} controlId="no">
                        <Form.Label>Apellido</Form.Label>
                        <Form.Control disabled type="string" value={props.serviceOrder["usuarioApellido"]} />
                    </Form.Group>
                </Row>
                <Row className="mb-3">
                    <Form.Group as={Col} controlId="no">
                        <Form.Label>Sector de la necesidad</Form.Label>
                        <Form.Control disabled value={props.serviceOrder["sector"]} />
                    </Form.Group>
                    <Form.Group as={Col} controlId="no">
                        <Form.Label>Categoría</Form.Label>
                        <Form.Control disabled value={props.serviceOrder["categoria"]} />
                    </Form.Group>
                </Row>
                <Form.Group className="mb-3" controlId="no">
                    <Form.Label>Descripción de la necesidad</Form.Label>
                    <Form.Control disabled as="textarea" rows={2} value={props.serviceOrder["descripcion"]} />
                </Form.Group>
                <Row className="mb-3">
                    <Form.Group as={Col} controlId="no">
                        <Form.Label>Estado</Form.Label>
                        <Form.Control disabled value={props.serviceOrder["estado"]} />
                    </Form.Group>
                    <Form.Group as={Col} controlId="no">
                        <Form.Label>Prioridad</Form.Label>
                        <Form.Control disabled value={props.serviceOrder["prioridad"]} />
                    </Form.Group>
                    
                    <Form.Group as={Col} controlId="no">
                        <Form.Label>Fecha de Necesidad</Form.Label>
                        <Form.Control disabled type="date" value={props.serviceOrder["fechaNecesidad"]} />
                    </Form.Group>
                </Row>
                <Form.Group className="mb-3" controlId="no">
                    <Form.Label>Comentario adicional</Form.Label>
                    <Form.Control disabled as="textarea" rows={2} value={props.serviceOrder["comentario"]===null?"":props.serviceOrder["comentario"]} />
                </Form.Group>
            </Col>
    )
}
