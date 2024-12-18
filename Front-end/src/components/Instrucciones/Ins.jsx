import React, { useState } from 'react';

const dropins = [
    {
        id: 1,
        titulo: "Pasos:",
        content: (
            <>
                <p>1. Descargar archivo .xlsx de Invas de "Historial LPN Cajas" con estado "TRX: Declarar PT".</p>
                <p>2. Abrir archivo llamado "HistorialCaja" y quitar formato completo de archivo.</p>
                <p>3. Subirlo a la plataforma y procesarlo.</p>
                <p>4. El archivo formateado estará listo para subir a Softland ERP.</p>
            </>
        ),
    },
    {
        id: 2,
        titulo: "Recomendaciones:",
        content: (
            <>
                <p>1. Revisar bien el valor del folio generado.</p>
                <p>2. Valida que la fecha se haya generado correctamente.</p>
            </>
        ),
    },
    
    {
        id: 2,
        titulo: "Funcionalidades:",
        content: (
            <>
                <p>1.   Formatear archivo PT de Invas a Softland.</p>
                <p>2.   Cambios de número de folio.</p>
                <p>3.   Consola de Logs.</p>
            </>
        ),
    },
];

const Ins = () => {
    const [activeIndex, setActiveIndex] = useState(null);

    const toggleContent = (index) => {
        if (activeIndex === index) {
            setActiveIndex(null); // Close if clicked again
        } else {
            setActiveIndex(index); // Open selected content
        }
    };

    return (
        <div className="py-4 mt-2">
            <div>
                {/* Título */}
                <h1 className="text-white text-4xl font-bold mx-4">Instrucciones</h1>

                {/* Mapa de desplegables */}
                {dropins.map((item, index) => (
                    <div key={item.id}>
                        <div
                            className="cursor-pointer py-2 px-4 text-white font-semibold text-xl bg-teal-600 hover:bg-teal-400 rounded mt-4 w-full"
                            onClick={() => toggleContent(index)}
                        >
                            <h2>{item.titulo}</h2>
                        </div>

                        {activeIndex === index && (
                            <div className="text-white font-semibold text-base mx-12 mt-2">
                                {item.content}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Ins;
