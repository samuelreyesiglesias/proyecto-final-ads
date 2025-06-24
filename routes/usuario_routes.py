from flask import Blueprint, render_template, request, redirect, session, flash
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

usuario_blueprint = Blueprint('usuario', __name__)

def conectar_bd():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Verificar sesión
def sesion_requerida():
    if 'usuario' not in session:
        flash("Debes iniciar sesión para continuar.", "warning")
        return False
    return True

# Ruta principal de usuarios
@usuario_blueprint.route('/usuarios')
def usuarios():
    if not sesion_requerida():
        return redirect('/login')

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios)

# Agregar usuario
@usuario_blueprint.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    nombre = request.form['nombre']
    carnet = request.form['carnet']
    contrasena = request.form['contrasena']
    rol = request.form['rol']

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuario (nombre_usuario, carnet, contrasena, rol) VALUES (%s, %s, %s, %s)",
                   (nombre, carnet, contrasena, rol))
    conn.commit()
    conn.close()

    flash("Usuario agregado exitosamente.", "success")
    return redirect('/usuarios')

# Mostrar formulario de edición
@usuario_blueprint.route('/usuarios/editar/<int:id>')
def editar_usuario(id):
    if not sesion_requerida():
        return redirect('/login')

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect('/usuarios')

    return render_template('editar_usuario.html', usuario=usuario)

# Actualizar usuario
@usuario_blueprint.route('/usuarios/actualizar', methods=['POST'])
def actualizar_usuario():
    nombre = request.form['nombre']
    carnet = request.form['carnet']
    id_usuario = request.form['id_usuario']
    contrasena = request.form['contrasena']
    rol = request.form['rol']

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuario 
        SET nombre_usuario = %s, carnet = %s, contrasena = %s, rol = %s 
        WHERE id_usuario = %s
    """, (nombre, carnet, contrasena, rol, id_usuario))
    conn.commit()
    conn.close()

    flash("Usuario actualizado correctamente.", "info")
    return redirect('/usuarios')

# Eliminar usuario
@usuario_blueprint.route('/usuarios/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id,))
    conn.commit()
    conn.close()

    flash("Usuario eliminado correctamente.", "danger")
    return redirect('/usuarios')

 