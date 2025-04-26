// src/services/municipioService.js

const API_URL = '/api/municipios';

export async function obtenerMunicipios() {
  const res = await fetch(API_URL);
  return res.json();
}

export async function crearMunicipio(data) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function actualizarMunicipio(id, data) {
  const res = await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function eliminarMunicipio(id) {
  const res = await fetch(`${API_URL}/${id}`, {
    method: 'DELETE',
  });
  return res.json();
}
