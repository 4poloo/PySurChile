import React, { useState, useEffect } from 'react';
import Logsection from './../Log_Api/APILOG'; // Componente de logs

const Loader = () => {
    const [file, setFile] = useState(null); // Archivo seleccionado
    const [logs, setLogs] = useState([]); // Registros de logs
    const [isCheckboxChecked, setIsCheckboxChecked] = useState(false); // Estado del checkbox
    const [currentFolio, setCurrentFolio] = useState(null); // Folio actual del config.json
    const [newFolio, setNewFolio] = useState(''); // Folio ingresado por el usuario

    // Función para obtener el folio actual del backend
    useEffect(() => {
        const fetchCurrentFolio = async () => {
            try {
                const response = await fetch('/ultimo-folio'); // Ruta del endpoint en el backend
                if (!response.ok) throw new Error('Error al obtener el folio actual');
                const data = await response.json();
                setCurrentFolio(data.ultimo_folio); // Actualizar el folio actual
            } catch (error) {
                console.error(error);
                addLog('error', 'No se pudo obtener el folio actual.');
            }
        };

        fetchCurrentFolio();
    }, []);

    // Maneja el cambio del checkbox
    const handleCheckboxChange = (event) => {
        setIsCheckboxChecked(event.target.checked);
    };

    // Maneja el cambio del textbox
    const handleTextboxChange = (event) => {
        setNewFolio(event.target.value);
    };

    // Enviar el nuevo folio al backend
    const applyNewFolio = async () => {
        try {
            const response = await fetch('/folio/', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nuevo_folio: parseInt(newFolio) }), // Enviar el nuevo folio
            });

            if (!response.ok) throw new Error('Error al actualizar el folio');
            const data = await response.json();
            addLog('success', `Folio actualizado: ${data.nuevo_folio}`);
            setCurrentFolio(data.nuevo_folio); // Actualizar el folio actual en el frontend
        } catch (error) {
            console.error(error);
            addLog('error', 'No se pudo actualizar el folio.');
        }
    };

    // Maneja el cambio de archivo
    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile?.type === 'text/csv') {
            const reader = new FileReader();
            reader.onload = () => {
                const content = reader.result;
                const isUtf8 = checkUtf8Encoding(content);
                if (!isUtf8) {
                    alert('El archivo no está en formato UTF-8. Asegúrate de guardarlo correctamente.');
                    setFile(null);
                } else {
                    setFile(selectedFile);
                }
            };
            reader.readAsText(selectedFile);
        } else {
            alert('Por favor seleccione un archivo .CSV válido.');
        }
    };

    const checkUtf8Encoding = (content) => {
        try {
            decodeURIComponent(escape(content));
            return true;
        } catch (e) {
            return false;
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
            alert('Por favor seleccione un archivo antes de transformar.');
            return;
        }
        const formData = new FormData();
        formData.append('file', file);
    };

    const clearLogs = () => {
        setLogs([]);
    };

    const addLog = (status, message) => {
        setLogs((prevLogs) => [...prevLogs, { status, message }]);
    };

    return (
        <div className="flex flex-col items-center bg-gray-800 py-6">
            {/* Opciones del folio */}
            <div className="w-full max-w-lg p-6 mt-4 bg-gray-300 border-2 border-black rounded-lg shadow-lg hover:border-yellow-400">
                <label className="flex items-center space-x-2">
                    <input
                        type="checkbox"
                        checked={isCheckboxChecked}
                        onChange={handleCheckboxChange}
                        className="form-checkbox"
                    />
                    <span className="text-gray-800 font-semibold">Cambiar número de folio inicial</span>
                </label>

                {isCheckboxChecked && (
                    <div className="mt-4 space-y-2">
                        <p className="text-gray-800">Folio actual: <span className="font-bold">{currentFolio}</span></p>
                        <input
                            type="number"
                            value={newFolio}
                            onChange={handleTextboxChange}
                            placeholder="Nuevo folio"
                            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                        />
                        <button
                            onClick={applyNewFolio}
                            className="w-full py-2 bg-primary/80 hover:bg-secondary/80 text-white font-semibold rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                            Aplicar Configuración
                        </button>
                    </div>
                )}
            </div>
            <label className='text-3xl font-semibold text-white py-2'>Sistema de carga</label>
            <div className="w-full max-w-lg p-6 bg-gray-300 border-2 hover:border-yellow-400 border-black rounded-lg shadow-lg">
                <h1 className="text-xl font-semibold text-center mb-4">Subir Excel de Invas</h1>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="flex justify-center">
                        <input
                            type="file"
                            accept=".csv"
                            onChange={handleFileChange}
                            className="hidden"
                            id="fileinput"
                        />
                        <label htmlFor="fileinput" className="cursor-pointer py-2 px-4 bg-primary/80 hover:bg-secondary/80 text-white font-semibold rounded-md shadow-sm">
                            Seleccionar Archivo
                        </label>
                    </div>
                    {file && (
                        <p className="text-gray-600 text-center">
                            Archivo seleccionado: <span className="font-medium">{file.name}</span>
                        </p>
                    )}
                    <button
                        type="submit"
                        className="w-full py-2 bg-primary/80 hover:bg-secondary/80 text-white font-semibold rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                        Transformar
                    </button>
                </form>
            </div>
            <div className="mt-2 w-full max-w-lg">
                <Logsection logs={logs} clearLogs={clearLogs} />
            </div>
        </div>
    );
};

export default Loader;
