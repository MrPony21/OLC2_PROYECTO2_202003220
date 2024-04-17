import { func } from 'prop-types';
import React, { useState } from 'react';

let datosTabla = []

export function actualizarErrores(nuevosDatos){
    datosTabla = nuevosDatos
    console.log('ha', datosTabla)
}
  
  const Errores = () => {
    
    return (
      <div className="tabla">
        <h2>Tabla de Errores</h2>
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Descripcion</th>
              <th>Ambito</th>
              <th>linea</th>
              <th>columna</th>
              <th>tipo</th>
            </tr>
          </thead>
          <tbody>
            {/* Mapea sobre los datos y crea filas de la tabla */}
            {datosTabla.map((item, index) => (
              <tr key={index}>
                <td>{index + 1 }</td>
                <td>{item.descripcion}</td>
                <td>{item.ambito}</td>
                <td>{item.linea}</td>
                <td>{item.column}</td>
                <td>{item.tipo}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

export default Errores;
