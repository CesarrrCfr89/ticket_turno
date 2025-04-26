# app/controladores/login_controlador.py
# app/controladores/login_controlador.py
import hashlib
from app.modelos.admin_model import AdminModel

class LoginControlador:
    def __init__(self):
        self.modelo = AdminModel()

    def login_valido(self, usuario, contrasena):
        usuario_data = self.modelo.obtener_usuario_por_username(usuario)
        
        if usuario_data:
            # Encriptar la contraseña ingresada
            contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

            # Comparar con la que está en la base de datos
            if usuario_data[2] == contrasena_hash:  # Asumiendo que el campo de contraseña es la columna 2
                return {'usuario': usuario_data[1], 'rol': usuario_data[3]}  # Ajusta según tus columnas

        return None
