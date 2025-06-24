from flask import Blueprint, render_template, request, redirect, session, flash
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

login_blueprint = Blueprint('login', __name__)

def conectar_bd():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Mostrar formulario de login
@login_blueprint.route('/login')
def login():
    return render_template('login.html')

# Procesar inicio de sesión
@login_blueprint.route('/login', methods=['POST'])
def login_post():
    carnet = request.form['carnet']
    contrasena = request.form['contrasena']

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE carnet = %s AND contrasena = %s", (carnet, contrasena))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        session['usuario'] = usuario['nombre_usuario']
        session['rol'] = usuario['rol']
        flash("Bienvenido/a, " + usuario['nombre_usuario'], "success")
        return redirect('/dashboard')
    else:
        flash("Credenciales incorrectas. Intenta de nuevo.", "danger")
        return redirect('/login')

# Cerrar sesión
@login_blueprint.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect('/login')

@login_blueprint.route('/')
@login_blueprint.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'], rol=session['rol'])
    else:
        flash("Por favor, inicia sesión primero.", "warning")
        return redirect('/login')