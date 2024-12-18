import React from 'react'
import CD from './components/Status/CD'
import LD from './components/Loader/Loader'
import TT from './components/Instrucciones/Ins'

function App() {
  return (
    <div className='w-full h-full bg-gray-800' >
      <CD />        
      <TT />
      <LD />      {/* Pagina de carga Excel */}
    </div>
  )
}

export default App
