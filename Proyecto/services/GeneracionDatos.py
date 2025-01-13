from pymongo import MongoClient
from faker import Faker
from services.mongo_service import MongoService
import random

def generar_datos(): 

    client = MongoService()
    # Configurar la conexión a MongoDB
    db = client.db
    pacientes_col = db["pacientes"]
    medicos_col = db["medicos"]
    citas_col = db["citas"]

    # Generar datos aleatorios para pacientes
    fake = Faker()
    pacientes = []

    for _ in range(10):


        pacientes.append({
            "nombre": fake.name(),
            "DNI": f"{random.randint(10000000, 99999999)}{random.choice('TRWAGMYFPDXBNJZSQVHLCKE')}",
            "edad": random.randint(18, 90),
            "direccion": fake.address(),
            "telefono": "6" + str(random.randint(0,99999999)),
            "email": fake.email()
        })
    pacientes_col.insert_many(pacientes)

    # Generar datos aleatorios para médicos
    especialidades = ["Cardiología", "Dermatología", "Pediatría", "Neurología", "Oncología"]

    medicos = []
    for _ in range(5):

        medicos.append({
            "nombre": fake.name(),
            "DNI": f"{random.randint(10000000, 99999999)}{random.choice('TRWAGMYFPDXBNJZSQVHLCKE')}",
            "especialidad": random.choice(especialidades),
            "telefono": "6" + str(random.randint(0,99999999)),
            "email": fake.email()
        })
    medicos_col.insert_many(medicos)

    # Generar datos aleatorios para citas
    citas = []
    for _ in range(20):
        citas.append({

            "id_paciente": random.choice(pacientes)["DNI"],  # Referencia a paciente
            "id_medico": random.choice(medicos)["DNI"],     # Referencia a médico
            "fecha": fake.date_time_this_year(),
            "motivo": fake.sentence(nb_words=6),
            "nro_cita":f"{random.randint(10000000, 99999999)}"
        })
    citas_col.insert_many(citas)

    print("Datos generados e insertados correctamente.")

def menu():

    while True:
        
        print("\n--- Menú Principal ---")
        print("1. Generar datos")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            generar_datos()
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu()
