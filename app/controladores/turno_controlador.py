import sqlite3
from fpdf import FPDF
from flask import render_template, request, redirect, url_for




def registrar_turno(datos):
    import sqlite3

    # Obtener los datos del formulario
    curp = datos['curp'].strip().upper()
    nombre = datos['nombre']
    apellido_paterno = datos['apellido_paterno']
    apellido_materno = datos['apellido_materno']
    telefono = datos['telefono']
    celular = datos['celular']
    correo = datos['correo']
    nivel = datos['nivel']
    municipio = datos['municipio'].strip().upper()
    asunto = datos['asunto']

    # Conexión a la base de datos con 'with' para asegurar cierre automático
    conn = sqlite3.connect("app/base_datos.db")
    conn.row_factory = sqlite3.Row  # Acceso por nombre de columna
    cursor = conn.cursor()

        # Obtener el último turno asignado para ese municipio
    cursor.execute("SELECT MAX(turno) AS max_turno FROM solicitudes_turno WHERE municipio = ?", (municipio,))
    resultado = cursor.fetchone()
    ultimo_turno = resultado["max_turno"] if resultado["max_turno"] is not None else 0
    nuevo_turno = ultimo_turno + 1

        # Insertar nueva solicitud de turno
    cursor.execute(''' 
            INSERT INTO solicitudes_turno (
                curp, nombre, apellido_paterno, apellido_materno,
                telefono, celular, correo, nivel, municipio, asunto, turno
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            curp,
            nombre,
            apellido_paterno,
            apellido_materno,
            telefono,
            celular,
            correo,
            nivel,
            municipio,
            asunto,
            nuevo_turno
        ))

    conn.commit()  # Commit para guardar los cambios
    conn.close()  # Cerrar la conexión

    return nuevo_turno  # Devolver el turno asignado


def modificar_turno(request):
    # Obtener los datos del formulario
    datos = request.form.to_dict()
    curp = datos['curp'].strip().upper()
    turno = datos['turno']

    # Conexión a la base de datos
    conn = sqlite3.connect("app/base_datos.db")
    cursor = conn.cursor()

    # Verificar si el CURP y el número de turno existen
    cursor.execute("SELECT * FROM solicitudes_turno WHERE curp = ? AND turno = ?", (curp, turno))
    registro = cursor.fetchone()

    if registro:
        # Si existe el registro, actualizamos los datos
        cursor.execute('''
            UPDATE solicitudes_turno
            SET nombre = ?, apellido_paterno = ?, apellido_materno = ?, telefono = ?, celular = ?, correo = ?, nivel = ?, municipio = ?, asunto = ?
            WHERE curp = ? AND turno = ?
        ''', (
            datos['nombre'],
            datos['apellido_paterno'],
            datos['apellido_materno'],
            datos['telefono'],
            datos['celular'],
            datos['correo'],
            datos['nivel'],
            datos['municipio'],
            datos['asunto'],
            curp,
            turno
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('turno.vista_turno'))  # Redirige a una página de éxito o confirmación

    else:
        conn.close()
        return "No se encontró el registro con ese CURP y número de turno.", 404 