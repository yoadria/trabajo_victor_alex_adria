from services.mongo_service import MongoService
import re

db = MongoService()

def validacion_id(collection_name, dni):
    try:
        collection = db.get_collection(collection_name)
        if collection.find_one({"DNI": dni}) is not None:
            raise Exception("Error: ya existe otra persona con el mismo DNI")
    except Exception as e:
        raise Exception(f"Error al validar ID: {str(e)}")


def validar_email(email):
    """
    Valida el formato de un email
    """
    # Expresión regular para validar un email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Comparar la expresión regular con el email
    if re.match(regex, email):
        return True
    else:
        return False
    

def validar_telefono(telefono):
    """
    Valida si un número de teléfono tiene exactamente 9 dígitos
    """
    # Expresión regular para 9 dígitos
    regex = r'^\d{9}$'

    # Comparar la expresión regular con el número de teléfono
    if re.match(regex, telefono):
        return True
    else:
        return False
    

def validar_dni(dni):
    # Expresión regular para 8 dígitos seguidos de una letra
    patron = r"^\d{8}[a-zA-Z]$"
    
    if re.match(patron, dni):
        return True
    else:
        return False
    
def validar_edad(edad):
    try:
        int(edad) 
        return True
    except ValueError:  
        return False