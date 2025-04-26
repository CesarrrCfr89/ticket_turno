# app/modelos/admin_model.py

import sqlite3
import hashlib
import os


class AdminModel:
    def __init__(self):
        self.db_path = 'app/base_datos.db'  # Ruta de tu base de datos SQLite

    def obtener_usuario_por_username(self, username):
        # Crear una conexión a la base de datos
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Ejecutar la consulta SQL para obtener el usuario por nombre de usuario
        cursor.execute("SELECT * FROM administradores WHERE usuario = ?", (username,))
        
        # Recuperar el primer resultado
        usuario = cursor.fetchone()

        # Cerrar la conexión a la base de datos
        conn.close()

        # Retornar el resultado, o None si no se encontró
        return usuario