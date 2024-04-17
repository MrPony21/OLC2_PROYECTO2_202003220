import { func } from 'prop-types';
import React, { useState } from 'react';

let datosTabla = []

export function actualizarDatosTabla(nuevosDatos){
    datosTabla = nuevosDatos
}
  
  const TablaDeSimbolos = () => {
    
    return (
      <div className="tabla">
        <h2>Tabla de Símbolos</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Tipo de Símbolo</th>
              <th>Tipo de Dato</th>
              <th>Ámbito</th>
              <th>Línea</th>
              <th>Columna</th>
            </tr>
          </thead>
          <tbody>
            {/* Mapea sobre los datos y crea filas de la tabla */}
            {datosTabla.map(item => (
              <tr key={item.ID}>
                <td>{item.ID}</td>
                <td>{item.Tipo_simbolo}</td>
                <td>{item["Tipo de dato"]}</td>
                <td>{item.Ambito}</td>
                <td>{item.linea}</td>
                <td>{item.columna}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

export default TablaDeSimbolos;
