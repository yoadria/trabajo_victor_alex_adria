from pymongo import MongoClient
from bson.objectid import ObjectId
# from datetime import datetime

# Modelos
class Paciente:
    
    def __init__(self, nombre: str, dni: str, edad: int, direccion: str, telefono: str, email: str):
        self.nombre = nombre
        self.dni = dni
        self.edad = edad
        # self.genero = genero
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

class Medico:
    
    def __init__(self, nombre: str, dni: str, especialidad: str, telefono: str, email: str):
        self.nombre = nombre
        self.dni = dni
        self.especialidad = especialidad
        self.telefono = telefono
        self.email = email

class Cita:
    
    def __init__(self, id_paciente: str, nro_cita: int, id_medico: str, fecha: str, motivo: str):
        self.id_paciente = id_paciente
        self.nro_cita = nro_cita
        self.id_medico = id_medico
        self.fecha = fecha
        self.motivo = motivo
