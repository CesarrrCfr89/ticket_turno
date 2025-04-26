
from flask import Flask

from flask_cors import CORS

def crear_app():
    app = Flask(__name__)
    
    # Habilitar CORS para todas las rutas que empiezan con /api/
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    app.secret_key = 'clave_secreta_para_captcha'

    # Importar rutas
    from app.rutas.login_rutas import login_bp
    from app.rutas.turno_rutas import turno_bp
    from app.rutas.municipios_rutas import municipios_bp
    

    app.register_blueprint(login_bp)
    app.register_blueprint(turno_bp)
    app.register_blueprint(municipios_bp)
  

    return app
