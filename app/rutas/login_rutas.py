from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from app.controladores.login_controlador import LoginControlador
import random

login_bp = Blueprint('login', __name__)
controlador = LoginControlador()

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect(url_for('turno.vista_turno'))  # Redirigir si ya hay sesión

    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        captcha = request.form['captcha']
        captcha_esperado = session.get('captcha_valor')

        # Verificar captcha
        if captcha != str(captcha_esperado):
            flash("Captcha incorrecto.")
            return redirect(url_for('login.login'))

        # Verificar credenciales
        usuario_data = controlador.login_valido(usuario, contrasena)

        if usuario_data:
            session['usuario'] = usuario  # Guardar nombre de usuario en la sesión
            flash("Login exitoso")
            return redirect(url_for('turno.vista_turno'))
        else:
            flash("Usuario o contraseña incorrectos.")
            return redirect(url_for('login.login'))

    # Generar captcha
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    session['captcha_valor'] = num1 + num2

    return render_template("login.html", num1=num1, num2=num2)

@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))
