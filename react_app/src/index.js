import React, { useState } from "react";
import ReactDOM from "react-dom";
import { NavBar } from "./navbar";
import  TablaDeSimbolos  from "./tabla"
import { Principal } from "./principal";
import Errores from "./errores"
import DevData from "./devdata"

import "./style.css";

const root = ReactDOM.createRoot(document.getElementById("root"));


function App() {
    const [mostrarTabla, setMostrarTabla] = useState(false);
    const [mostrarInicio, setMostrarInicio] = useState(true);
    const [mostrarErrores, setmostrarErrores] = useState(false);
    const [mostrarDev, setmostrarDev] = useState(false)


    const mostrarTablaHandler = (mostrar) => {
        setMostrarTabla(mostrar);
        setMostrarInicio(false); // Oculta el componente Principal si se muestra la tabla
        setmostrarErrores(false)
        setmostrarDev(false)
    };

    const mostrarErroreshandler = (mostrar) =>{
        setmostrarErrores(mostrar)
        setMostrarInicio(false)
        setMostrarTabla(false)
        setmostrarDev(false)
    }

    const mostrarDevData = (mostrar) => {
        setmostrarDev(mostrar)
        setmostrarErrores(false)
        setMostrarInicio(false)
        setMostrarTabla(false)

    }

    return (
        <>
            <NavBar mostrarTabla={mostrarTablaHandler} mostrarInicio={setMostrarInicio} mostrarErrores={mostrarErroreshandler} mostrarDev={mostrarDevData}/>
            {mostrarInicio && <Principal />}
            {mostrarTabla && <TablaDeSimbolos/>}
            {mostrarErrores && <Errores/>}
            {mostrarDev && <DevData/>}
        </>
    );
}

root.render(<App />);
