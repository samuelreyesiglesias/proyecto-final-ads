# modelo.py

class Asistencia:
    def __init__(self, id_asistencia, id_estudiante, id_asignatura, fecha, estado):
        self.id_asistencia = id_asistencia
        self.id_estudiante = id_estudiante
        self.id_asignatura = id_asignatura
        self.fecha = fecha
        self.estado = estado  # Ejemplo: "Presente", "Ausente", "Tarde"
