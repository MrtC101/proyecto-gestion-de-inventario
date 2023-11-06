import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import axios, { AxiosHeaders, AxiosResponse } from "axios"
import {BASEURL, getBackendUrl} from "../data/BACKENDURLS"
import { getNav } from '../components/CRUDComponents/navComp/navComp'

const inventarioAPI = axios.create()
//inventarioAPI.defaults.xsrfCookieName = 'csrftoken';
//inventarioAPI.defaults.xsrfHeaderName = 'X-CSRFToken';
inventarioAPI.defaults.withCredentials = true;
inventarioAPI.defaults.baseURL = BASEURL

export function ListItems(setItems : any, itemName : string) : Promise<AxiosResponse<any,any>> {
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
        async function loadItems() {
            await inventarioAPI.get(getBackendUrl(itemName))
            .then((response) => {
                setItems(response.data);
                resolve(response)
            })
            .catch((error )=>(error.response?.status !== 403? reject(error):getNav()("/login")))
        }
        loadItems()
    });
}

export function ReadItem(setItem:any,itemName:string) : Promise<AxiosResponse<any,any>> {
    const {id} = useParams();
    console.log(getBackendUrl(itemName) + `${id}/`)
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
        useEffect(() => {
            async function loadItem(){
                await inventarioAPI.get(
                    getBackendUrl(itemName)+`${id}/`
                )
                .then((response) => {
                    setItem(response.data)
                    resolve(response)
                })
                .catch((error )=>(error.response?.status !== 403? reject(error):getNav()("/login")))
            }
            loadItem()
        }, [itemName, setItem]);
    })
}

export function CreateItem(itemName: string, formData: FormData | string) : Promise<AxiosResponse<any,any>> {
    console.log(formData);
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
        async function createData(itemName: string, formData: FormData) {
            await inventarioAPI.post(getBackendUrl(itemName), formData)
            .then((response) => resolve(response))
            .catch((error )=>(error.response?.status !== 403? reject(error):getNav()("/login")))
        }
        createData(itemName, formData);
    })
}


export function UpdateItem(itemName:string,formData:FormData,id:string|undefined) : Promise<AxiosResponse<any,any>> {   
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
        async function updateData(itemName:string,id:string|undefined,formData:FormData){
            await inventarioAPI.put(getBackendUrl(itemName) +`${id}/`, formData)
            .then((response) => resolve(response))
            .catch((error )=>(error.response?.status !== 403? reject(error):getNav()("/login")))
        }
        updateData(itemName, id, formData)
    })
}

export function DeleteItem(itemName: string, id: string) : Promise<AxiosResponse<any,any>> {
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
        async function deleteData(itemName: string, id: string) {
            await inventarioAPI.delete(getBackendUrl(itemName) +`${id}/`)
            .then((response) => resolve(response))
            .catch((error )=>(error.response?.status !== 403? reject(error):getNav()("/login")))
        }
        deleteData(itemName, id);
    })
}

export function getSectors(setSectors : any,edificioName : number) : Promise<AxiosResponse<any,any>> {
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
        async function listSectors() {
            await inventarioAPI.get(`tarea/sector/subsectores/${edificioName}/`)
            .then((response) => {
                setSectors(response.data);
                resolve(response);
            })
            .catch((error )=>(error.response?.status !== 403? reject(error):getNav()("/login")))
        }
        listSectors();
    })
}

export function SendServiceRequest(formData: FormData) : Promise<AxiosResponse<any,any>> {
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
        async function sendData(formData: FormData) {
            await inventarioAPI.post(getBackendUrl("ordenes-servicio"), formData)
            .then((response) => resolve(response))
            .catch((error )=>(error.response?.status !== 403? reject(error):getNav()("/login")))
        }
        sendData(formData);
    })
}

export function GetEnums(setEnum:any) : Promise<AxiosResponse<any,any>> {
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
            
            async function loadItem(){
                await inventarioAPI.get(getBackendUrl("enums"))
                .then((response) => {
                    setEnum(response.data)
                    resolve(response)
                    
                })
                .catch((error)=>(error.response?.status !== 403? reject(error):getNav()("/login")))
            }
            loadItem();
            
        });
}

export function ListItemsFiltered(setItems, filteredEntityName, filterID){
    console.log(`${filteredEntityName}-filtered`)
    return new Promise<AxiosResponse<any,any>>((resolve,reject) => {
        async function loadItems() {
            await inventarioAPI.get(getBackendUrl(`${filteredEntityName}-filtered`).concat(`${filterID}/`))
            .then((response) => {
                setItems(response.data);
                resolve(response)
            })
            .catch((error )=>(error.response?.status !== 403? reject(error):getNav()("/login")))
        }
        loadItems()
    });
}

export function getToken(){
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function requestToken() {
            await inventarioAPI.get('/usuario/csrf/')
            .then((response) => {
                console.log(response)
                inventarioAPI.defaults.headers.common['X-CSRFToken'] = response.headers['X-CSRFToken'];
                resolve(response)
            })
            .catch((error)=>(reject(error)))
        }
        requestToken();
    });
}

export function Login(formData: FormData): Promise<AxiosResponse<any, any>> {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        async function loginUser() {
            await inventarioAPI.post('/usuario/login/', formData)
            .then((response) => {
                resolve(response)
            })
            .catch((error)=>(reject(error)))
        }
        loginUser();
    });
}
