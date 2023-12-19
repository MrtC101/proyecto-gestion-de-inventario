import "./header.scss"
import { Button, ButtonGroup, Col, Container, Dropdown, ListGroup, ListGroupItem, Popover, PopoverBody, PopoverHeader, Row } from "react-bootstrap";

import { Logout, WhoAmI } from "../../../Api/apiService";

import { useAuthData } from "../../providerComponents/authProvider/AuthProvider";
import { setMessage } from "../../providerComponents/messageDisplay/MessageDisplay";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import DropdownItem from "react-bootstrap/esm/DropdownItem";

function UserDropDown(){
  const [authData,setAuthData] = useAuthData();
  const nav = useNavigate();
  const handleLogout = () => {
    Logout()
    .then(()  => {
      setAuthData(
        {
          authenticated: false,
          username: "No consultado",
          email: "No consultado",
          rol: "No consultado",
        }
      );
      nav("/login")
    })
    .catch(e=>{
      setMessage("Error al cerrar sesión",e)
    }) 
  }

  const [visible,setVisible]=useState(false);
  const ja = ()=>{
    setVisible(!visible)
  }
  return (
    <>
    <Dropdown as={ButtonGroup} drop="start">
      <Button className="user" variant="secondary">
        <img src="https://freesvg.org/img/abstract-user-flat-4.png" alt="" />
        <span>{authData['username']}</span>
      </Button>
      <Dropdown.Toggle split variant="secondary" id="dropdown-split-basic"/>
      <Dropdown.Menu>
      <div className="fields">
          <ListGroup>
            <ListGroupItem>
              <span className="header">Usuario: </span>
              <span className="content">{authData['username']}</span>
            </ListGroupItem>
            <ListGroupItem>
              <span className="header">Correo:</span>
              <span className="content">{authData['email']}</span>
            </ListGroupItem>
            <ListGroupItem>
              <span className="header">Rol: </span>
              <span className="content">{authData['rol']}</span>
            </ListGroupItem>
            <ListGroupItem>
            <Button variant="warning" onClick={()=>{nav("/nueva-contraseña")}}>Cambiar Contraseña</Button>  
            </ListGroupItem>
            <ListGroupItem>
            <Button variant="danger" onClick={handleLogout}>Cerrar sesión</Button>
            </ListGroupItem>
          </ListGroup>    
        </div>
      </Dropdown.Menu>
    
    </Dropdown>
    </>
  );
}


function Header() {
  return (
    <div className="myheader">
      <div className="logo">
        <img className="transparent" src="https://ingenieria.uncuyo.edu.ar/images/ingenieriablanco2016.png" alt="" />
        <span>Mantenimiento</span>
      </div>
      <div className="icons">
        <UserDropDown/> 
      </div>
    </div>
  );
}

export default Header