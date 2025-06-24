from flask import Blueprint, render_template, request, redirect, session, flash
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

asistencia_blueprint = Blueprint('asistencia', __name__)

def conectar_bd():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Ruta para listar todas las asistencias
@asistencia_blueprint.route('/asistencias')
def listar_asistencias():
    if 'usuario' not in session:
        return redirect('/login')
    
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.id_asistencia, e.nombre AS estudiante, a.presente AS presente, a.fecha, a.presente
        FROM asistencia a
        JOIN estudiante e ON a.id_estudiante = e.id_estudiante
        ORDER BY a.fecha DESC
    """)
    #JOIN asignatura s ON a.id_asignatura = s.id_asignatura
    asistencias = cursor.fetchall()

    cursor.execute("SELECT id_estudiante, nombre FROM estudiante")
    estudiantes = cursor.fetchall()

    cursor.execute("SELECT id_asignatura, nombre FROM asignatura")
    asignaturas = cursor.fetchall()

    conn.close()
    return render_template('asistencias.html', asistencias=asistencias, estudiantes=estudiantes, asignaturas=asignaturas)

# Ruta para agregar nueva asistencia
@asistencia_blueprint.route('/asistencias/agregar', methods=['POST'])
def agregar_asistencia():
    id_estudiante = request.form['id_estudiante']
    id_asignatura = request.form['id_asignatura']
    fecha = request.form['fecha']
    presente = request.form.get('presente') == 'on'  # Checkbox

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO asistencia (id_estudiante, id_asignatura, fecha, presente)
        VALUES (%s, %s, %s, %s)
    """, (id_estudiante, id_asignatura, fecha, presente))
    conn.commit()
    conn.close()

    flash("✅ Asistencia registrada correctamente.", "success")
    return redirect('/asistencias')

# Ruta para eliminar una asistencia
@asistencia_blueprint.route('/asistencias/eliminar/<int:id>',methods=['POST'])
def eliminar_asistencia(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM asistencia WHERE id_asistencia = %s", (id,))
    conn.commit()
    conn.close()

    flash("🗑️ Asistencia eliminada correctamente.", "info")
    return redirect('/asistencias')

# Ruta para mostrar el formulario de edición
@asistencia_blueprint.route('/asistencias/editar/<int:id>')
def editar_asistencia(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM asistencia WHERE id_asistencia = %s", (id,))
    asistencia = cursor.fetchone()

    cursor.execute("SELECT * FROM estudiante where id_estudiante = %s", (asistencia['id_estudiante'],))
    estudiantes = cursor.fetchall()

    

    conn.close()

    if not asistencia:
        flash("❌ Asistencia no encontrada.", "warning")
        return redirect('/asistencias')

    return render_template('editar_asistencia.html', asistencia=asistencia, estudiantes=estudiantes )

# Ruta para actualizar una asistencia
@asistencia_blueprint.route('/asistencias/actualizar/<int:id>', methods=['POST'])
def actualizar_asistencia(id):
    fecha = request.form['fecha']
    presente = request.form.get('presente') == 'on'

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE asistencia 
        SET   fecha = %s, presente = %s 
        WHERE id_asistencia = %s
    """, ( fecha, presente, id))
    conn.commit()
    conn.close()

    flash("✏️ Asistencia actualizada correctamente.", "success")
    return redirect('/asistencias')
