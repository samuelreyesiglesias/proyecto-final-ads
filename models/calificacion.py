# modelo.py

class Calificacion:
    def __init__(self, id_calificacion, id_estudiante, id_asignatura, nota, periodo):
        self.id_calificacion = id_calificacion
        self.id_estudiante = id_estudiante
        self.id_asignatura = id_asignatura
        self.nota = nota
        self.periodo = periodo
