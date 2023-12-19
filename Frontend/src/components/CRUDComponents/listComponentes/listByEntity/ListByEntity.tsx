import "./listByEntity.scss"
import { PureComponent, useEffect, useRef, useState } from "react";
import { Button, Card, ListGroup } from "react-bootstrap";
import { FixedSizeList } from 'react-window';
import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import { DataGrid, GridColDef, GridToolbar } from "@mui/x-data-grid";

import { ListItems, ListItemsFiltered } from "../../../../Api/apiService"

import ModalForm, { FormType } from "../../createComponents/modalForm/ModalForm";;
import DeleteAlert from "../deleteAlert/DeleteAlert";
import { DataTable } from "../dataTable/DataTable";

import { setMessage } from "../../../providerComponents/messageDisplay/MessageDisplay";

import { getPlural, getSingular } from "../../../../data/TRANSLATIONS";
import { Field, GetColumns, GetFields } from "../../../../data/STRUCTURE";
import getACTION from "../../../../data/ACTIONS";


function FilteredDataGrid({ filterID, filteredEntity,  setFilterID }): React.ReactElement {
    const [openAdd, setOpenAdd] = useState(false);
    const [openUpdate, setOpenUpdate] = useState(false);
    const [openRead, setOpenRead] = useState(false);
    const [openDelete, setOpenDelete] = useState(false);
    
    const [row, setRow]: [Record<string, any>, any] = useState([]);

    const changeRef = useRef(false);

    const switchChange = () => {
        changeRef.current = !changeRef.current;
    }

    const [items, setItems] = useState([]);

    useEffect(()=>{
        if(filterID>=0){
            ListItemsFiltered(setItems, filteredEntity, filterID)
            .catch((error) => {
                setMessage(`Ha surgido un error al buscar ${getPlural(filteredEntity)}.`,error)
            })
        }
    }, [changeRef.current, filteredEntity, setFilterID,filterID])

    const columns: GridColDef[] = GetColumns("compra", filteredEntity);
    const fields: Field[] = GetFields("compra", filteredEntity);

    return (
        <>
            <div className="myTable col">
                <div className="info">
                    {(getACTION(filteredEntity)["add"]) && <button className="btn btn-primary mb-2" onClick={() => setOpenAdd(true)}>Agregar {getSingular(filteredEntity)}</button>}
                </div>

                <DataTable slug={filteredEntity} columns={columns} rows={items} setOpenUpdate={setOpenUpdate} setOpenRead={setOpenRead} setOpenDelete={setOpenDelete} setRow={setRow} />

                {openAdd && <ModalForm slug={filteredEntity} fields={fields} setOpen={setOpenAdd} formType={FormType.ADD} row={null} switchChange={switchChange} />}
                {openUpdate && <ModalForm slug={filteredEntity} fields={fields} setOpen={setOpenUpdate} formType={FormType.UPDATE} row={row} switchChange={switchChange} />}
                {openRead && <ModalForm slug={filteredEntity} fields={fields} setOpen={setOpenRead} formType={FormType.READ} row={row} switchChange={switchChange} />}
                {openDelete && <DeleteAlert slug={filteredEntity} id={row["id"]} setOpen={setOpenDelete} switchChange={switchChange} />}
            </div>
        </>

    )
}

function ListFilters({ setFilterID, filterName }): React.ReactElement {

    const [filters, setFilters] = useState([]);

    useEffect(() => {
        ListItems(setFilters, filterName)
            .catch((error) => {
                setMessage(`Ha surgido un error al buscar ${getPlural(filterName)}.`, error)
            })
    }, [setFilters])

    const [currWord,setCurrWord] = useState("");

    const handleClick = (filter) => setFilterID(filter["id"]);
    const lookFor = (filter) => String(filter["id"]).startsWith(currWord) 
    || (new Date(filter["fechaHora"])).toLocaleString().match(currWord) 
    || currWord === "";

    return (
        <div className="Filters col-2">
            <Card>
                <h4>Pedidos de Insumo</h4>
                <Card className="custom-card">
                    <input value={currWord} placeholder="Buscar..." onChange={(event) => setCurrWord(event.target.value)}/>
                    <div style={{ maxHeight: '65vh', overflowY: 'auto' }}>
                    <ListGroup>
                    {
                        filters.filter(lookFor).map((filter,index) => {
                            return (
                                <ListItem className="list-items" key={index}>
                                    <ListItemButton className="btn btn-primary" onClick={() => handleClick(filter)}>
                                        <ListItemText className="item-button-id" primary={filter["id"]} />
                                        <ListItemText className="item-button-date" primary={`${(new Date(filter["fechaHora"])).toLocaleString()}`} />
                                    </ListItemButton>
                                </ListItem>
                            )
                        })
                    }
                    </ListGroup>
                     </div>
               </Card>
            </Card>
        </div>
    );
}

const ListByEntity = ({ entityNameToFilterBy, entityNameToList }) => {
    const ErrorState = useState(["", false]);
    
    // Operaciones de etnidad
    const [filterID, setFilterID] = useState(-1);
    console.log(filterID)
    return (
        <>
           <div className="ListByEntity">
            <div className="col">
                <h1 className="row title">{getPlural(entityNameToList)}</h1>
                <div className="row">
                    <ListFilters setFilterID={setFilterID} filterName={entityNameToFilterBy} />
                    <FilteredDataGrid filterID={filterID} filteredEntity={entityNameToList} setFilterID={setFilterID} />

                </div>

            </div>
            
            </div>
            
        </>
    );
}

export default ListByEntity;