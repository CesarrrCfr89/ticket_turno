import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MunicipiosPage from './pages/MunicipiosPage';
import MunicipiosCrud from './components/MunicipiosCrud';


function App() {
  return (
    <div className="App">
    <h1>Gestión de Municipios</h1>
    <MunicipiosCrud />
  </div>
  );
}

export default App
