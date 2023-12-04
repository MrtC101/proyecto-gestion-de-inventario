import "./login.scss";
import React, { useContext, useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Link, useNavigate } from 'react-router-dom';

import { WhoAmI ,Login as login } from "../../Api/apiService"
import { useAuthData } from "../../components/providerComponents/authProvider/AuthProvider";
import { setMessage } from "../../components/providerComponents/messageDisplay/MessageDisplay";
import MessageDisplay from "../../components/providerComponents/messageDisplay/MessageDisplay";

function Login() {
  
  const [authData,setAuthData] = useAuthData();
  const [validated,setValidated] = useState(false);
  const nav = useNavigate();
  
  const handleWhoAmI = () => {
      WhoAmI()
      .then((r)=>{
        setAuthData({
          id:r.data["id"],
          authenticated: true,
          username: r.data["username"],
          email: r.data["email"],
          rol: r.data["rol"]
        });
        if(r.data["default_password"]){
          nav("/nueva-contraseña")
        }else if(r.data["is_staff"]){
          nav("/")
        }else{
          nav("/orden-servicio")
        }
      })
      .catch((e)=>{
        setMessage("Error al cargar usuario",e)
      })
  }
  

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const formData = new FormData(form);
    
    if (form.checkValidity() === false) {
      e.stopPropagation();
    } else {
      login(formData)
      .then((r)=>{
        handleWhoAmI();
      })
      .catch((e)=>(
        setMessage("Error al iniciar sesión",e)
      ))
    }
  };

  function LoginForm(){
    return (
      <div className="container foreground">
        <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <div className="header">
              <div className="text">Log In</div>
              <div className="underline"></div>
            </div>
            
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Usuario</Form.Label>
              <Form.Control name="username" type="string" placeholder="Ingrese nombre de usuario" />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Contraseña</Form.Label>
              <Form.Control name="password" type="password" placeholder="Contraseña" />
            </Form.Group>
            
            <div className="d-grid">
              <Button className="btn btn-dark btn-lg btn-block" type="submit">
                Ingresar
              </Button>
            </div>
            
            <p className="text-end mt-2">
              <Link to="" className="ms-2">¿Olvidaste tu contraseña?</Link>
            </p>
          </Form>
      </div>
    );
  }

  return (
    <>
      <div className="error">
        <MessageDisplay />
      </div>
      <div className="background">    
        <LoginForm/>
      </div>
    </>          
  )
}

export default Login
