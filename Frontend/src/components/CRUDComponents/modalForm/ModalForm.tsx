import "./modalForm.scss"
import { useState } from "react";

import { GetUrlParts, UpdateItem as Update, CreateItem as Create } from "../../../Api/apiService"
import { getSingular } from "../../../data/data";
import { setMessage } from "../messageDisplay/MessageDisplay";
import { Field } from "../getColumns/GetColumns";
import Button from 'react-bootstrap/Button'
import SelectList from "../selectList/SelectList";

import Form from 'react-bootstrap/Form';

const mesureUnits = [
    "litro",
    "metro",
    "gramo",
    "contable"
]

export enum FormType {
    ADD = "add",
    UPDATE = "update"
}

type Props = {
    slug: string,
    fields: Field[],
    setOpen: React.Dispatch<React.SetStateAction<boolean>>,
    formType: FormType,
    row: [Record<string, any>, any] | null
    switchChange: () => void,
}


const ModalForm = (props: Props) => {
    
    const { item: itemName, module: moduleName } = GetUrlParts();

    const [validated, setValidated] = useState(false);

    const updateItem = (item: string, formData: FormData, id: number) => {
        // Comentario jm: sería mejor que la función reciba un int y el casteo lo haga dentro
        Update(item, formData, id.toString())
        .then(() => {
            setMessage(`Se ha modificado ${getSingular(item)} con éxito`, false)
        })
        .catch((error) => {
            setMessage(`Ha surgido un error al modificar ${getSingular(item)}`, true)
        })
        .finally(() => props.setOpen(false));
    }

    const createItem = (item: string, formData:FormData) => {
        Create(item, formData)
        .then(() => {
            setMessage(`Se ha creado el nuevo ${getSingular(item)} con exito`, false)
        })
        .catch((error) => {
            setMessage(`Ha surgido un error al crear el Nuevo ${getSingular(item)}`, true)
        })
        .finally(() => props.setOpen(false));
    }


    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const form = e.currentTarget as HTMLFormElement;
        const formData = new FormData(form);
        
        if (form.checkValidity() === false) {
            e.stopPropagation();
        }
        setValidated(true);
        
        if (props.formType === FormType.UPDATE) {
            if (props.row != null)
            updateItem(itemName, formData, props.row["id"]);
        } else {
            createItem(itemName, formData);
        }   
    };
    
    const mesureUnits = [
        "litro",
        "metro",
        "gramo",
        "contable"
    ]
    return (
        <div className="add">
            <div className="modal2">
                <div className="close">
                    <button className="btn dark" onClick={() => props.setOpen(false)}>X</button>
                </div>
                {props.formType === FormType.ADD ? (
                    <h1>Crear nuevo {getSingular(props.slug)}</h1>
                ):(
                    <h1>Modificar {getSingular(props.slug)}</h1>
                )}
                <Form noValidate validated={validated} onSubmit={handleSubmit}>
                    {props.fields
                        .filter(item => item.field !== "id")
                        .map((field, index) => {
                            return (
                                <Form.Group className="form-group" key={index}>
                                    <Form.Label>{field.headerName}</Form.Label>
                                    {field.enum ? (
                                        field.field === "unidadMedida" ? (
                                            <Form.Select
                                                name="unidadMedida"
                                                className="form-select"
                                                required>
                                                <option defaultValue={(props.formType === FormType.UPDATE && props.row !== null) ? 
                                                    (props.row["unidadMedida"]) : ("")}
                                                 value="" disabled>Elegir unidad de medida</option>
                                                {mesureUnits.map(unidad => (
                                                    <option value={unidad} key={unidad}>{unidad}</option>
                                                ))}
                                            </Form.Select>
                                        ):(
                                            <SelectList 
                                                fieldName={field.field}
                                                defaultValue={(props.formType === FormType.UPDATE && props.row !== null) ? 
                                                    (props.row[field.field]) : ("")} />
                                            
                                        )
                                    ):(
                                        <Form.Control
                                            name={field.field}
                                            required={field.required ? true : false}
                                            type={field.type}
                                            placeholder={`Ingrese ${field.headerName}`}
                                            defaultValue={(props.formType === FormType.UPDATE && props.row!==null) ? (
                                                props.row[field.field]):("")}
                                        />
                                    )}
                                    {field.required ? (
                                        <Form.Control.Feedback type="invalid">
                                            Este campo es obligatorio
                                        </Form.Control.Feedback>
                                    ):(<Form.Control.Feedback />)}
                                </Form.Group>
                            )
                        })
                    }
                    {(props.formType === FormType.ADD) && <Button type="submit" className="mt-3" onClick={() => props.switchChange()}>Crear</Button>}
                    {(props.formType === FormType.UPDATE) && <Button type="submit" className="mt-3" onClick={() => props.switchChange()}>Modificar</Button>}
                </Form>
            </div>
        </div>
    );
}

export default ModalForm; 