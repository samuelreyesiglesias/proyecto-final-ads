from flask import Blueprint, render_template, request, redirect, session, flash
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

estudiante_blueprint = Blueprint('estudiante', __name__)

def conectar_bd():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Mostrar todos los estudiantes
@estudiante_blueprint.route('/estudiantes')
def listar_estudiantes():
    if 'usuario' not in session:
        return redirect('/login')

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estudiante ORDER BY nombre")
    estudiantes = cursor.fetchall()
    conn.close()
    
    return render_template('estudiantes.html', estudiantes=estudiantes)

# Agregar estudiante
@estudiante_blueprint.route('/estudiantes/agregar', methods=['POST'])
def agregar_estudiante():
    nombre = request.form['nombre'] 
    grado = request.form['grado']

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO estudiante (nombre,  grado)
        VALUES (%s, %s)
    """, (nombre,  grado))
    conn.commit()
    conn.close()

    flash("✅ Estudiante agregado correctamente.", "success")
    return redirect('/estudiantes')

# Eliminar estudiante
from mysql.connector import IntegrityError

@estudiante_blueprint.route('/estudiantes/eliminar/<int:id>', methods=['POST'])
def eliminar_estudiante(id):
    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM estudiante WHERE id_estudiante = %s", (id,))
        if cursor.rowcount == 0:
            flash("❌ Estudiante no encontrado.", "warning")
        else:
            conn.commit()
            flash("✅ Estudiante eliminado correctamente.", "success")

    except IntegrityError as e:
        # El estudiante tiene registros relacionados (asistencia, calificación, etc.)
        flash("⚠️ No se puede eliminar el estudiante porque tiene registros asociados (asistencia, notas, etc.).", "danger")

    finally:
        conn.close()
        return redirect('/estudiantes')

# Mostrar formulario para editar
@estudiante_blueprint.route('/estudiantes/editar/<int:id>')
def editar_estudiante(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estudiante WHERE id_estudiante = %s", (id,))
    estudiante = cursor.fetchone()
    
    #estudiantes
    cursor.execute("SELECT id_estudiante, nombre FROM estudiante")
    estudiantes = cursor.fetchall()
    #asignaturas

    conn.close()




    if not estudiante:
        flash("❌ Estudiante no encontrado.", "warning")
        return redirect('/estudiantes')

    return render_template('editar_estudiante.html', estudiante=estudiante, estudiantes = estudiantes)

# Actualizar datos del estudiante
@estudiante_blueprint.route('/estudiantes/actualizar/<int:id>', methods=['POST'])
def actualizar_estudiante(id):
    nombre = request.form['nombre'] 
    grado = request.form['grado']

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE estudiante
        SET nombre = %s,   grado = %s
        WHERE id_estudiante = %s
    """, (nombre,  grado, id))
    conn.commit()
    conn.close()

    flash("✏️ Datos actualizados correctamente.", "success")
    return redirect('/estudiantes')
