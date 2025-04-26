import sqlite3
import hashlib

# Ruta a la base de datos
ruta_db = "app/base_datos.db"

# Conexión y cursor
conn = sqlite3.connect(ruta_db)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS administradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL
);
''')

# Insertar un admin de prueba con usuario: admin, contraseña: admin123
usuario = "admin"
contrasena_plana = "admin123"
contrasena_hash = hashlib.sha256(contrasena_plana.encode()).hexdigest()

cursor.execute("INSERT OR IGNORE INTO administradores (usuario, contrasena) VALUES (?, ?)",
               (usuario, contrasena_hash))

# Guardar y cerrar
conn.commit()
conn.close()

print("✔ Tabla creada e inserción realizada correctamente.")
