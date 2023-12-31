import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios, { AxiosHeaders, AxiosResponse } from "axios"
import { BASEURL, getBackendUrl } from "../data/BACKENDURLS"
import { initializedNavegate as nav } from "../components/providerComponents/navProvider/NavProvider";

const inventarioAPI = axios.create()
inventarioAPI.defaults.xsrfCookieName = 'csrftoken';
inventarioAPI.defaults.xsrfHeaderName = 'X-CSRFToken';
//inventarioAPI.defaults.headers.common['X-CSRFToken'] = 'token';
//Activa el intercambio de sesiones,credenciales y cookies en las peticiones
inventarioAPI.defaults.withCredentials = true;
//Coloca la ip correspondiente como url base para todas las peticiones.
inventarioAPI.defaults.baseURL = BASEURL


function backToLogin(){
    sessionStorage.clear();
    nav("/login");   
}

export function ListItems(setItems: any, itemName: string): Promise<AxiosResponse<any, any>> {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function loadItems() {
            await inventarioAPI.get(getBackendUrl(itemName))
                .then((response) => {
                    setItems(response.data);
                    
                    resolve(response)
                })
                .catch(
                    //(error) => reject(error)
                    (error) => (error.response?.status !== 403 ? reject(error) : backToLogin(nav))
                    )
        }
        loadItems()
    });
}

export function ReadItem(setItem: any, itemName: string): Promise<AxiosResponse<any, any>> {
    const { id } = useParams();

    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        useEffect(() => {
            async function loadItem() {
                await inventarioAPI.get(
                    getBackendUrl(itemName) + `${id}/`
                )
                    .then((response) => {
                        setItem(response.data)
                        resolve(response)
                    })
                    .catch(
                        //(error) => reject(error)
                        (error) => (error.response?.status !== 403 ? reject(error) : backToLogin())                    
                    )    
                    }
            loadItem()
        }, [itemName, setItem, id]);
    })
}


export function ReadItemId(setItem: any, itemName: string, id: string): Promise<AxiosResponse<any, any>> {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        
        async function loadItem() {
            await inventarioAPI.get(
                getBackendUrl(itemName) + `${id}/`
            )
                .then((response) => {
                    setItem(response.data)
                    resolve(response)
                })
                .catch(
                    (error) => reject(error)
                    /*(error) => (error.response?.status !== 403 ? reject(error) : nav("/login"))*/)
        }
        loadItem()
        
    })
}




export function CreateItem(itemName: string, formData: FormData | string): Promise<AxiosResponse<any, any>> {
    
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function createData(itemName: string, formData: FormData) {
            await inventarioAPI.post(getBackendUrl(itemName), formData)
                .then((response) => {
                    resolve(response)
                })
                .catch(
                    (error) => (error.response?.status !== 403 ? reject(error) : backToLogin())                                        
                )
        }
        createData(itemName, formData);
    })
}


export function UpdateItem(itemName: string, formData: FormData, id: string | undefined): Promise<AxiosResponse<any, any>> {
    
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function updateData(itemName: string, id: string | undefined, formData: FormData) {
            await inventarioAPI.put(getBackendUrl(itemName) + `${id}/`, formData)
                .then((response) => {
                    
                    resolve(response)
                })
                .catch(
                    (error) => (error.response?.status !== 403 ? reject(error) : backToLogin())                    
                )
        }
        updateData(itemName, id, formData)
    })
}

export function DeleteItem(itemName: string, id: string): Promise<AxiosResponse<any, any>> {
    
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function deleteData(itemName: string, id: string) {
            await inventarioAPI.delete(getBackendUrl(itemName) + `${id}/`)
                .then((response) => {
                    
                    resolve(response)
                })
                .catch(
                (error) => (error.response?.status !== 403 ? reject(error) : backToLogin()) 
                )                   
            }
        deleteData(itemName, id);
    })
}

export function getSectors(setSectors: any, edificioName: number): Promise<AxiosResponse<any, any>> {
    
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function listSectors() {
            await inventarioAPI.get(`tarea/sector/subsectores/${edificioName}/`)
                .then((response) => {
                    setSectors(response.data);
                    
                    resolve(response);
                })
                .catch(
                (error) => (error.response?.status !== 403 ? reject(error) : backToLogin())  
                )                  
        }
        listSectors();
    })
}

export function SendServiceRequest(formData: FormData): Promise<AxiosResponse<any, any>> {
    
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function sendData(formData: FormData) {
            await inventarioAPI.post(getBackendUrl("ordenes-servicio"), formData)
                .then((response) => {
                    
                    resolve(response)
                })
                .catch(
                    (error) => (error.response?.status !== 403 ? reject(error) : backToLogin())                                        
                )
            }
        sendData(formData);
    })
}

export function GetEnums(setEnum: any): Promise<AxiosResponse<any, any>> {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function loadItem() {
            await inventarioAPI.get(getBackendUrl("enums"))
                .then((response) => {
                    setEnum(response.data)
                    resolve(response)
                })
                .catch(
                    (error) => reject(error)
                /*(error) => (error.response?.status !== 403 ? reject(error) : ("/login"))*/
                )
        }
        loadItem();

    });
}

export function ListItemsFiltered(setItems, filteredEntityName, filterID) {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function loadItems() {
            await inventarioAPI.get(getBackendUrl(`${filteredEntityName}-filtered`).concat(`${filterID}/`))
                .then((response) => {
                    setItems(response.data);
                    
                    resolve(response)
                })
                .catch(
                    (error) => (error.response?.status !== 403 ? reject(error) : backToLogin())  
                    ) 
        }
        loadItems()
    });
}

export function Login(formData: FormData): Promise<AxiosResponse<any, any>> {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function loginUser() {
            await inventarioAPI.post('/usuario/login/', formData)
                .then((response) => {
                    
                    resolve(response)
                })
                .catch((error) => (reject(error)))
        }
        loginUser();
    });
}

export function newPassword(formData: FormData): Promise<AxiosResponse<any, any>> {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function loginUser() {
            await inventarioAPI.post('/usuario/change_password/', formData)
                .then((response) => {
                    
                    resolve(response)
                })
                .catch((error) => (reject(error)))
        }
        loginUser();
    });
}

export function WhoAmI() {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function whoami() {
            await inventarioAPI.get('/usuario/whoami/')
                .then((response) => {
                    resolve(response)
                })
                .catch((error) => (reject(error)))
        }
        whoami();
    });
}

export function Logout() {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function loginUser() {
            await inventarioAPI.post('/usuario/logout/')
                .then((response) => {
                    resolve(response)
                })
                .catch(
                    (error) => backToLogin() 
                    ) 
        }
        loginUser();
    });
}