const express = require('express');
const app = express();
const cors = require('cors');
const bodyParser = require('body-parser');
const municipiosRoutes = require('./routes/municipiosRoutes');

// Configuración
app.use(cors());
app.use(bodyParser.json()); // Para que el servidor pueda entender JSON

// Usar rutas de municipios
app.use('/api', municipiosRoutes);

// Iniciar el servidor
app.listen(5000, () => {
  console.log('Servidor corriendo en el puerto 5000');
});
