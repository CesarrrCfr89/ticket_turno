import os
import qrcode
from flask import Blueprint, render_template, request, send_file,redirect,url_for
from app.controladores.turno_controlador import registrar_turno
from fpdf import FPDF
import sqlite3

turno_bp = Blueprint('turno', __name__)

@turno_bp.route("/solicitud_turno")
def vista_turno():
    municipios = obtener_municipios()
    return render_template("solicitud_turno.html", municipios=municipios)

def obtener_municipios():
    # Si los municipios están en la base de datos
    conn = sqlite3.connect("app/base_datos.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Si tienes una tabla de municipios, cambia el nombre de la tabla
    cursor.execute("SELECT nombre FROM municipios")
    municipios = cursor.fetchall()
    
    conn.close()

    # Si los municipios están en un archivo de texto
    # municipios = []
    # with open('municipios.txt', 'r') as f:
    #     municipios = [line.strip() for line in f]

    return [municipio['nombre'] for municipio in municipios]

@turno_bp.route("/modificar_turno", methods=["GET", "POST"])
def modificar_turno_route():
    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "buscar":
            curp = request.form['curp'].strip().upper()
            turno = request.form['turno']

            conn = sqlite3.connect("app/base_datos.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM solicitudes_turno WHERE curp = ? AND turno = ?", (curp, turno))
            registro = cursor.fetchone()
            conn.close()

            if registro:
                turno_encontrado = {
                    'curp': registro['curp'],
                    'nombre': registro['nombre'],
                    'apellido_paterno': registro['apellido_paterno'],
                    'apellido_materno': registro['apellido_materno'],
                    'telefono': registro['telefono'],
                    'celular': registro['celular'],
                    'correo': registro['correo'],
                    'nivel': registro['nivel'],
                    'municipio': registro['municipio'],
                    'asunto': registro['asunto'],
                    'turno': registro['turno']
                }
                return render_template('modificar_turno.html', turno_encontrado=turno_encontrado)
            else:
                return "No se encontró el registro con ese CURP y turno.", 404

        elif accion == "actualizar":
            datos = request.form
            conn = sqlite3.connect("app/base_datos.db")

            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE solicitudes_turno SET 
                    nombre = ?, 
                    apellido_paterno = ?, 
                    apellido_materno = ?, 
                    telefono = ?, 
                    celular = ?, 
                    correo = ?, 
                    nivel = ?, 
                    municipio = ?, 
                    asunto = ?
                WHERE curp = ? AND turno = ?
            """, (
                datos['nombre'],
                datos['apellido_paterno'],
                datos['apellido_materno'],
                datos['telefono'],
                datos['celular'],
                datos['correo'],
                datos['nivel'],
                datos['municipio'],
                datos['asunto'],
                datos['curp'],
                datos['turno']
            ))

            conn.commit()
            conn.close()
            return "Turno actualizado correctamente"

    return render_template("modificar_turno.html")



@turno_bp.route("/registrar_turno", methods=["POST"])
def registrar_turno_route():
    datos = request.form

    # Obtener el turno asignado desde el controlador
    turno_asignado = registrar_turno(datos)

    # Crear el QR con la CURP
    qr_img = qrcode.make(datos['curp'])
    static_dir = os.path.join(os.getcwd(), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    qr_path = os.path.join(static_dir, 'qr_temp.png')
    qr_img.save(qr_path)

    # Crear el PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Comprobante de Turno", ln=True, align='C')
    pdf.cell(200, 10, txt=f"CURP: {datos['curp']}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre: {datos['nombre']} {datos['apellido_paterno']} {datos['apellido_materno']}", ln=True)
    pdf.cell(200, 10, txt=f"Turno asignado: {turno_asignado}", ln=True)
    pdf.cell(200, 10, txt=f"Municipio: {datos['municipio']}", ln=True)

    # Agregar el código QR
    pdf.image(qr_path, x=10, y=pdf.get_y() + 10, w=40, h=40)

    # Guardar el PDF
    pdf_output_path = os.path.join(static_dir, 'comprobante_turno.pdf')
    pdf.output(pdf_output_path)

    # Eliminar QR temporal (opcional)
    os.remove(qr_path)

    # Enviar el PDF
    return send_file(
        pdf_output_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name="comprobante_turno.pdf"
    )

@turno_bp.route('/consultar_turno', methods=['GET', 'POST'])
def consultar_turno_route():
    if request.method == 'POST':
        # Lógica para buscar registros por CURP o nombre
        query = request.form['query']
        
        # Aquí debes realizar la consulta de base de datos según el parámetro recibido
        conn = sqlite3.connect("app/base_datos.db")
        cursor = conn.cursor()
        
        # Si buscas por CURP
        cursor.execute("SELECT * FROM solicitudes_turno WHERE curp LIKE ?", ('%' + query + '%',))
        registros = cursor.fetchall()
        
        conn.close()

        return render_template('consultar_turno.html', registros=registros)
    
    return render_template('consultar_turno.html', registros=[])


@turno_bp.route("/modificar_turno/<int:turno_id>", methods=["GET", "POST"])
def modificar_turno(turno_id):
    conn = sqlite3.connect("app/base_datos.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Obtener los datos del turno
    cursor.execute("SELECT * FROM solicitudes_turno WHERE id = ?", (turno_id,))
    turno = cursor.fetchone()

    if request.method == "POST":
        # Recoger los datos del formulario
        curp = request.form['curp'].strip().upper()
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        telefono = request.form['telefono']
        celular = request.form['celular']
        correo = request.form['correo']
        nivel = request.form['nivel']
        municipio = request.form['municipio'].strip().upper()
        asunto = request.form['asunto']
        estatus = request.form['estatus']

        # Actualizar en la base de datos
        cursor.execute('''
            UPDATE solicitudes_turno SET
                curp = ?, nombre = ?, apellido_paterno = ?, apellido_materno = ?,
                telefono = ?, celular = ?, correo = ?, nivel = ?, municipio = ?, 
                asunto = ?, estatus = ?
            WHERE id = ?
        ''', (
            curp, nombre, apellido_paterno, apellido_materno,
            telefono, celular, correo, nivel, municipio,
            asunto, estatus, turno_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for('turno.consultar_turno_route'))

    
    return render_template("modificar_turno.html", turno=turno)


@turno_bp.route("/eliminar_turno/<int:turno_id>", methods=["POST"])
def eliminar_turno(turno_id):
    conn = sqlite3.connect("app/base_datos.db")
    cursor = conn.cursor()

    # Eliminar el turno
    cursor.execute("DELETE FROM solicitudes_turno WHERE id = ?", (turno_id,))
    
    conn.commit()
    conn.close()

    return redirect(url_for('turno.consultar_turno_route'))



@turno_bp.route("/cambiar_estatus/<int:turno_id>/<estatus>", methods=["GET"])
def cambiar_estatus(turno_id, estatus):
    conn = sqlite3.connect("app/base_datos.db")
    cursor = conn.cursor()

    # Actualizar el estatus
    cursor.execute("UPDATE solicitudes_turno SET estatus = ? WHERE id = ?", (estatus, turno_id))
    
    conn.commit()
    conn.close()

    return redirect(url_for('turno.consultar_turno_route'))


 


