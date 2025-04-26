import sqlite3

ruta_db = "app/base_datos.db"

conn = sqlite3.connect(ruta_db)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS solicitudes_turno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curp TEXT NOT NULL,
    nombre TEXT NOT NULL,
    apellido_paterno TEXT NOT NULL,
    apellido_materno TEXT,
    telefono TEXT,
    celular TEXT,
    correo TEXT,
    nivel TEXT,
    municipio TEXT NOT NULL,
    asunto TEXT,
    turno INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

conn.commit()
conn.close()

print("✔ Tabla solicitudes_turno creada correctamente.")
