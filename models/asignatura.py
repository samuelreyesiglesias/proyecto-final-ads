# modelo.py

class Asignatura:
    def __init__(self, id_asignatura, nombre, codigo, tipo, area):
        self.id_asignatura = id_asignatura
        self.nombre = nombre
        self.codigo = codigo
        self.tipo = tipo      # Ej: "Obligatoria" u "Optativa"
        self.area = area      # Ej: "Matemática", "Lenguaje"
