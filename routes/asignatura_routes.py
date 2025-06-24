from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

asignatura_blueprint = Blueprint('asignatura', __name__)

def conectar_bd():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Ruta para listar todas las asignaturas
@asignatura_blueprint.route('/asignaturas')
def listar_asignaturas():
    if 'usuario' not in session:
        return redirect('/login')
    
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM asignatura")
    asignaturas = cursor.fetchall()
    conn.close()

    return render_template('asignaturas.html', asignaturas=asignaturas)

# Ruta para agregar una nueva asignatura
@asignatura_blueprint.route('/asignaturas/agregar', methods=['POST'])
def agregar_asignatura():
    nombre = request.form['nombre']
    codigo = request.form['codigo']
    tipo = request.form['tipo']
    area = request.form['area']

    conn = conectar_bd()
    cursor = conn.cursor()

    # Validación para evitar códigos duplicados
    cursor.execute("SELECT * FROM asignatura WHERE codigo = %s", (codigo,))
    existente = cursor.fetchone()
    if existente:
        flash(f"⚠️ El código {codigo} ya está registrado.", "danger")
        conn.close()
        return redirect('/asignaturas')

    cursor.execute("INSERT INTO asignatura (nombre, codigo, tipo, area) VALUES (%s, %s, %s, %s)",
                   (nombre, codigo, tipo, area))
    conn.commit()
    conn.close()

    flash("✅ Asignatura registrada correctamente.", "success")
    return redirect('/asignaturas')

# Ruta para eliminar una asignatura
# @asignatura_blueprint.route('/asignaturas/eliminar/<int:id>')
# def eliminar_asignatura(id):
#     conn = conectar_bd()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM asignatura WHERE id_asignatura = %s", (id,))
#     conn.commit()
#     conn.close()

#     flash("🗑️ Asignatura eliminada.", "info")
#     return redirect('/asignaturas')

# Ruta para mostrar el formulario de edición
@asignatura_blueprint.route('/asignaturas/editar/<int:id>')
def editar_asignatura(id):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM asignatura WHERE id_asignatura = %s", (id,))
    asignatura = cursor.fetchone()
    conn.close()

    if not asignatura:
        flash("❌ Asignatura no encontrada.", "warning")
        return redirect('/asignaturas')

    return render_template('editar_asignatura.html', asignatura=asignatura)

# Ruta para actualizar una asignatura editada
@asignatura_blueprint.route('/asignaturas/actualizar/<int:id>', methods=['POST'])
def actualizar_asignatura(id):
    nombre = request.form['nombre']
    codigo = request.form['codigo']
    tipo = request.form['tipo']
    area = request.form['area']

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE asignatura 
        SET nombre = %s, codigo = %s, tipo = %s, area = %s 
        WHERE id_asignatura = %s
    """, (nombre, codigo, tipo, area, id))
    conn.commit()
    conn.close()

    flash("✏️ Asignatura actualizada correctamente.", "success")
    return redirect('/asignaturas')


@asignatura_blueprint.route('/asignaturas/eliminar/<int:id>', methods=['POST'])
def eliminar_asignatura(id):
    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM asignatura WHERE id_asignatura = %s", (id,))
        if cursor.rowcount == 0:
            flash("❌ Asignatura no encontrada.", "warning")
        else:
            conn.commit()
            flash("✅ Asignatura eliminada correctamente.", "success")

    except Exception as e:
        # La asignatura tiene registros relacionados (asistencia, calificación, etc.)
        flash("⚠️ No se puede eliminar la asignatura porque tiene registros asociados (asistencia, notas, etc.).", "danger")

    finally:
        conn.close()
        return redirect('/asignaturas')