import React from 'react';
import './NavBar.css'; 

export function NavBar({ mostrarTabla, mostrarInicio, mostrarErrores, mostrarDev }) {
  const handleInicioClick = () => {
      mostrarTabla(false); // Oculta la tabla si está mostrada
      mostrarInicio(true); // Muestra el componente Principal
  };

  return (
      <nav className="navbar">
          <ul className="nav-list">
              <li><a href="#" onClick={handleInicioClick}>Inicio</a></li>
              <li><a href="#" onClick={() => mostrarTabla(true)}>Tabla de simbolos</a></li>
              <li><a href="#" onClick={() => mostrarErrores(true)}>Errores</a></li>
              <li><a href="#" onClick={() => mostrarDev(true)}>Acerca de</a></li>
          </ul>
      </nav>
  );
}
