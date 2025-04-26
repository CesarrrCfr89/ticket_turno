const municipioModel = require('../models/municipioModel');

// Obtener todos los municipios
const getMunicipios = async (req, res) => {
  try {
    const municipios = await municipioModel.getMunicipios();
    res.json(municipios);
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener los municipios' });
  }
};

// Agregar un municipio
const addMunicipio = async (req, res) => {
  const { nombre } = req.body;
  if (!nombre) {
    return res.status(400).json({ error: 'El nombre es obligatorio' });
  }

  try {
    const newId = await municipioModel.addMunicipio(nombre);
    res.status(201).json({ id: newId, nombre });
  } catch (error) {
    res.status(500).json({ error: 'Error al agregar el municipio' });
  }
};

// Actualizar un municipio
const updateMunicipio = async (req, res) => {
  const { id } = req.params;
  const { nombre } = req.body;

  if (!nombre) {
    return res.status(400).json({ error: 'El nombre es obligatorio' });
  }

  try {
    const rowsAffected = await municipioModel.updateMunicipio(id, nombre);
    if (rowsAffected > 0) {
      res.json({ id, nombre });
    } else {
      res.status(404).json({ error: 'Municipio no encontrado' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Error al actualizar el municipio' });
  }
};

// Eliminar un municipio
const deleteMunicipio = async (req, res) => {
  const { id } = req.params;

  try {
    const rowsAffected = await municipioModel.deleteMunicipio(id);
    if (rowsAffected > 0) {
      res.json({ message: 'Municipio eliminado' });
    } else {
      res.status(404).json({ error: 'Municipio no encontrado' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Error al eliminar el municipio' });
  }
};

module.exports = {
  getMunicipios,
  addMunicipio,
  updateMunicipio,
  deleteMunicipio
};
