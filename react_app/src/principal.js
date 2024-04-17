import './style.css'
import React, { useState, useRef, useEffect } from 'react'
import { ImUpload2, ImPlay3, ImFloppyDisk } from "react-icons/im";
import { actualizarDatosTabla } from './tabla';
import { actualizarErrores } from './errores';

export function Principal() {

    const [fileContent, setFileContent] = useState('');
    const [fileName, setFileName] = useState('')
    const [consoleout, setConsoleout] = useState('')
    const consoleref = useRef(null);

    useEffect(() => {
        const savedFileContent = localStorage.getItem('fileContent');
        if (savedFileContent) {
            setFileContent(savedFileContent);
        }

        const savedFileName = localStorage.getItem('fileName');
        if (savedFileName) {
            setFileName(savedFileName);
        }

        const savedConsoleout = localStorage.getItem('consoleout');
        if (savedConsoleout) {
            setConsoleout(savedConsoleout);
        }
    }, []);

    useEffect(() => {
        localStorage.setItem('fileContent', fileContent);
        localStorage.setItem('fileName', fileName);
        localStorage.setItem('consoleout', consoleout);
    }, [fileContent, fileName, consoleout]);

    const handleExamineClick = () => {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.olc';
        fileInput.style.display = 'none';
        fileInput.onchange = (event) => {
            const selectedFile = event.target.files[0];
            setFileName(selectedFile.name);
            if (selectedFile) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const content = e.target.result;
                    setFileContent(content);
                    console.log(e)
                };
                reader.readAsText(selectedFile);
            }
        };
        document.body.appendChild(fileInput);
        fileInput.click();
        document.body.removeChild(fileInput);
    };

    const handlesubmit = () => {
        console.log('contenido completo', fileContent);
        fetch('http://127.0.0.1:5000/traducir', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: fileContent }), // Enviar el texto completo al servidor
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setConsoleout(data.console);
            console.log(data.tabla)
            actualizarDatosTabla(JSON.parse(data.tabla))
            actualizarErrores(JSON.parse(data.errores))
            
            if (data.errores != "[]"){
                alert("Error para mas informacion dirijase a la pestaña de errores")
            }
            
        })
        .catch(error => {
            console.error(error);
        });


    }

    const saveToFile = () => {
        const element = document.createElement('a');
        const file = new Blob([fileContent], {type: 'text/plain'});
        element.href = URL.createObjectURL(file);
        element.download = 'miarchivo.olc';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    return (
        <div className='principal'>
            <div className="console">
                <input style={{ width: '43vh', fontSize: '2.5vh', }} value={fileName} ></input>
                <button style={{ marginLeft: '17px', fontSize: '2.5vh' }} onClick={handleExamineClick}> <ImUpload2/> Examinar</button>
                <button style={{ marginLeft: '17px', fontSize: '2.5vh' }} onClick={saveToFile}> <ImFloppyDisk/> Guardar</button>
                <button style={{ marginLeft: '17px', fontSize: '2.5vh' }} onClick={handlesubmit}> <ImPlay3/> Interpretar</button>

                <textarea
                    value={fileContent}
                    style={{
                        width: 'calc(100% - 15px)',
                        height: '35vh',
                        marginTop: '15px',
                        resize: 'none'
                    }}
                    onChange={e => setFileContent(e.target.value)}
                ></textarea>

                <textarea
                    value={consoleout}
                    ref={consoleref}
                    style={{
                        width: 'calc(100% - 15px)',
                        height: '35vh',
                        marginTop: '15px',
                        resize: 'none'
                    }}
                ></textarea>

            </div>
        </div>
    )
}
