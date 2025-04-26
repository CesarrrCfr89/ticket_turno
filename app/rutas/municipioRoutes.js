const express = require('express');
const router = express.Router();
const municipiosController = require('../controllers/municipiosController');

// Rutas para municipios
router.get('/municipios', municipiosController.getMunicipios);
router.post('/municipios', municipiosController.addMunicipio);
router.put('/municipios/:id', municipiosController.updateMunicipio);
router.delete('/municipios/:id', municipiosController.deleteMunicipio);

module.exports = router;
