from flask import Blueprint, render_template, request, redirect, session, flash
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

calificacion_blueprint = Blueprint('calificacion', __name__)

def conectar_bd():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Listar calificaciones
@calificacion_blueprint.route('/calificaciones')
def listar_calificaciones():
    if 'usuario' not in session:
        return redirect('/login')

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id_calificacion,e.grado, e.nombre AS estudiante, a.nombre AS asignatura,
               c.nota 
        FROM calificacion c
        JOIN estudiante e ON c.id_estudiante = e.id_estudiante
        JOIN asignatura a ON c.id_asignatura = a.id_asignatura
        
    """)
    calificaciones = cursor.fetchall()
 

    cursor.execute("SELECT id_estudiante, nombre FROM estudiante")
    estudiantes = cursor.fetchall()

    cursor.execute("SELECT id_asignatura, nombre FROM asignatura")
    asignaturas = cursor.fetchall()

    conn.close()
    return render_template('calificaciones.html', calificaciones=calificaciones,
                           estudiantes=estudiantes, asignaturas=asignaturas)

# Agregar calificación
@calificacion_blueprint.route('/calificaciones/agregar', methods=['POST'])
def agregar_calificacion():
    id_estudiante = request.form['id_estudiante']
    id_asignatura = request.form['id_asignatura']
    nota = request.form['nota']
    #fecha = request.form['fecha']
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO calificacion (id_estudiante, id_asignatura, nota)
            VALUES (%s, %s, %s)
        """, (id_estudiante, id_asignatura, nota))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"❌ Error al registrar la calificación: {err}", "danger")
        return redirect('/calificaciones')
    except Exception as e:
        flash(f"❌ Error inesperado: {e}", "danger")
        return redirect('/calificaciones')
    if not id_estudiante or not id_asignatura or not nota:
        flash("❌ Todos los campos son obligatorios.", "warning")
        return redirect('/calificaciones')
    

    flash("✅ Calificación registrada con éxito.", "success")
    return redirect('/calificaciones')

# Eliminar calificación
@calificacion_blueprint.route('/calificaciones/eliminar/<int:id>',methods=["POST"])
def eliminar_calificacion(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calificacion WHERE id_calificacion = %s", (id,))
    conn.commit()
    conn.close()

    flash("🗑️ Calificación eliminada correctamente.", "info")
    return redirect('/calificaciones')

# Editar calificación (mostrar formulario)
@calificacion_blueprint.route('/calificaciones/editar/<int:id>')
def editar_calificacion(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM calificacion WHERE id_calificacion = %s", (id,))
    calificacion = cursor.fetchone()

    cursor.execute("SELECT id_estudiante, nombre FROM estudiante where id_estudiante = %s", (calificacion['id_estudiante'],))
    estudiantes = cursor.fetchall()

    cursor.execute("SELECT id_asignatura, nombre FROM asignatura where id_asignatura = %s", (calificacion['id_asignatura'],))
    asignaturas = cursor.fetchall()

    conn.close()

    if not calificacion:
        flash("❌ Calificación no encontrada.", "warning")
        return redirect('/calificaciones')

    return render_template('editar_calificacion.html', calificacion=calificacion,
                           estudiantes=estudiantes, asignaturas=asignaturas)

# Actualizar calificación
@calificacion_blueprint.route('/calificaciones/actualizar/<int:id>', methods=['POST'])
def actualizar_calificacion(id):
    # id_estudiante = request.form['id_estudiante']
    # id_asignatura = request.form['id_asignatura']
    nota = request.form['nota']
    #fecha = request.form['fecha']

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE calificacion
        SET    nota = %s 
        WHERE id_calificacion = %s
    """, ( nota,  id))
    conn.commit()
    conn.close()

    flash("✏️ Calificación actualizada correctamente.", "success")
    return redirect('/calificaciones')
