import { DataGrid, GridColDef, GridToolbar} from "@mui/x-data-grid";
import "./dataTable.scss"
import { Link } from "react-router-dom";
import { BsTrash } from "react-icons/bs";
import { BiEdit } from "react-icons/bi";
import { HiOutlineEye } from "react-icons/hi";


type Props = {
    columns: GridColDef[],
    rows: object[],
    slug: string
}

const handleDelete = (id:number) => {
    // delete the item
    // axios.delete(`/api/${slug}/id)
    console.log(id + " has been deleted!")
}

export const DataTable = (props: Props) => {

    const actionColumn: GridColDef = {
        field: "action",
        headerName: "Action",
        width: 200,
        renderCell: (params) => {

            return(
                <div className="action">
                    <Link to={`/${props.slug}/${params.row.id}`}>
                        <img src="/view.svg" alt="" />
                    </Link>
                    <div className="delete" onClick={()=>handleDelete(params.row.id)}>
                        <img src="/delete.svg" alt="" />
                    </div>
                    <div>
                        <Link to={`Read/${params.row.id}`}>
                            <button><HiOutlineEye/></button>
                        </Link>
                    </div>
                    <div>
                        <Link to={`Update/${params.row.id}`}>
                        <button><BiEdit/></button>
                        </Link>
                    </div>
                    <div>
                        <Link to={`Delete/${params.row.id}`}>
                            <button><BsTrash/></button>
                        </Link>
                    </div>
                </div>  
            )
        }
    }    

    return (
        <div className="dataTable">
            <DataGrid
                className="dataGrid"
                rows={props.rows}
                columns={[...props.columns, actionColumn]}
                initialState={{
                    pagination: {
                        paginationModel: {
                            pageSize: 10,
                        },
                    },
                }}
                slots={{toolbar:GridToolbar}}
                slotProps={{
                    toolbar:{
                        showQuickFilter:true,
                        quickFilterProps:{debounceMs: 500},

                    }
                }}
                pageSizeOptions={[5]}
                checkboxSelection
                disableRowSelectionOnClick
            
                disableDensitySelector
                disableColumnSelector
                />
        </div>
    )
}