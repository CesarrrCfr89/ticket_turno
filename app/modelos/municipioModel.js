const db = require('../config/db');

// Obtener todos los municipios
const getMunicipios = () => {
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM municipios', (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
};

// Insertar un nuevo municipio
const addMunicipio = (nombre) => {
  return new Promise((resolve, reject) => {
    db.run('INSERT INTO municipios (nombre) VALUES (?)', [nombre], function (err) {
      if (err) reject(err);
      else resolve(this.lastID); // Devuelve el ID del municipio recién insertado
    });
  });
};

// Actualizar un municipio
const updateMunicipio = (id, nombre) => {
  return new Promise((resolve, reject) => {
    db.run('UPDATE municipios SET nombre = ? WHERE id = ?', [nombre, id], function (err) {
      if (err) reject(err);
      else resolve(this.changes); // Devuelve cuántas filas fueron afectadas
    });
  });
};

// Eliminar un municipio
const deleteMunicipio = (id) => {
  return new Promise((resolve, reject) => {
    db.run('DELETE FROM municipios WHERE id = ?', [id], function (err) {
      if (err) reject(err);
      else resolve(this.changes); // Devuelve cuántas filas fueron eliminadas
    });
  });
};

module.exports = {
  getMunicipios,
  addMunicipio,
  updateMunicipio,
  deleteMunicipio
};
