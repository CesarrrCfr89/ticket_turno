# app/rutas/municipios_rutas.py
# app/rutas/municipios_rutas.py

from flask import Blueprint, request, jsonify
import sqlite3
import os

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
municipios_bp = Blueprint('municipios', __name__, url_prefix='/api/municipios')

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'base_datos.db')

def conectar():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# GET: todos los municipios
@municipios_bp.route('/', methods=['GET'])
def obtener_municipios():
    con = conectar()
    if not con:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    
    cur = con.cursor()
    cur.execute("SELECT id, nombre FROM municipios")
    datos = cur.fetchall()
    con.close()

    if not datos:
        return jsonify({'mensaje': 'No se encontraron municipios'}), 404

    # Convertir cada fila en un diccionario para evitar los objetos sqlite3.Row
    municipios = [{'id': row[0], 'nombre': row[1]} for row in datos]
    response = jsonify(municipios)
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response

# GET: un municipio por ID
@municipios_bp.route('/<int:id>', methods=['GET'])
def obtener_municipio(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nombre FROM municipios WHERE id=?", (id,))
    row = cur.fetchone()
    con.close()

    if row:
        return jsonify({'id': row[0], 'nombre': row[1]})
    return jsonify({'error': 'Municipio no encontrado'}), 404

# POST: crear municipio
@municipios_bp.route('/', methods=['POST'])
def crear_municipio():
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({'error': 'Nombre requerido'}), 400

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO municipios (nombre) VALUES (?)", (nombre,))
        con.commit()
        nuevo_id = cur.lastrowid
        con.close()
        return jsonify({'id': nuevo_id, 'nombre': nombre}), 201
    except sqlite3.IntegrityError:
        
        return jsonify({'error': 'Ya existe ese municipio'}), 400

# PUT: actualizar municipio
@municipios_bp.route('/<int:id>', methods=['PUT'])
def actualizar_municipio(id):
    data = request.get_json()
    nombre = data.get('nombre')
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE municipios SET nombre=? WHERE id=?", (nombre, id))
    con.commit()
    con.close()
    return jsonify({'id': id, 'nombre': nombre})

# DELETE: eliminar municipio
@municipios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_municipio(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM municipios WHERE id=?", (id,))
    con.commit()
    con.close()
    return jsonify({'mensaje': 'Municipio eliminado'})

@dashboard_bp.route('/estatus', methods=['GET'])
def resumen_estatus():
    municipio_id = request.args.get('municipio_id')  # opcional
    con = conectar()
    cur = con.cursor()

    if municipio_id:
        cur.execute("""
            SELECT estatus, COUNT(*) 
            FROM solicitudes 
            WHERE municipio_id = ?
            GROUP BY estatus
        """, (municipio_id,))
    else:
        cur.execute("""
            SELECT estatus, COUNT(*) 
            FROM solicitudes 
            GROUP BY estatus
        """)

    datos = cur.fetchall()
    con.close()

    resultado = {row[0]: row[1] for row in datos}
    return jsonify(resultado)
