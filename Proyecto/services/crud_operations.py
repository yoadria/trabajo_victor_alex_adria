from .mongo_service import MongoService
from utils.validators import validacion_id

db = MongoService()

def insert_data(collection_name, data):
    """Inserta un documento en la colección especificada."""
    try:
        # Validar que el ID no exista previamente
        if collection_name != 'citas':
            if "DNI" not in data:
                raise ValueError("El campo 'DNI' es obligatorio para esta colección.")
            validacion_id(collection_name, data["DNI"])
        
        collection = db.get_collection(collection_name)
        result = collection.insert_one(data)
        return result.inserted_id

    except Exception as e:
        raise Exception(f"Error al insertar datos: {str(e)}")

def read_data(collection_name):
    """Obtiene todos los documentos de la colección especificada."""
    try:
        collection = db.get_collection(collection_name)
        datos = list(collection.find())
        if not datos:
            raise Exception(f"No se encontraron datos en la colección '{collection_name}'.")
        return datos

    except Exception as e:
        raise Exception(f"Error al obtener datos: {str(e)}")

def update_data(collection_name, query_filter, update_values):
    
    try:
        collection = db.get_collection(collection_name)

        # Validar que el documento existe antes de actualizar

        existing_document = collection.find_one(query_filter)

        if not existing_document:
            raise Exception(f"No se encontró el documento con el filtro: {query_filter}")
        
        # Realizar la actualización
        result = collection.update_one(query_filter, {"$set": update_values})
        
        if result.modified_count == 0:
            raise Exception("No se realizaron cambios, verifica los valores proporcionados.")
        
        return result

    except Exception as e:
        raise Exception(f"Error al actualizar datos: {str(e)}")
    
def delete_data(collection_name, query_filter):
    """
    Elimina un documento de la colección especificada según el filtro proporcionado.
    """
    try:
        collection = db.get_collection(collection_name)

        # Buscar el documento antes de eliminar
        existing_document = collection.find_one(query_filter)

        if not existing_document:
            raise Exception(f"No se encontró el documento con el filtro: {query_filter}")

        # Eliminar el documento
        result = collection.delete_one(query_filter)
        
        if result.deleted_count == 0:
            raise Exception("No se pudo eliminar el documento. Verifica los valores proporcionados.")
        
        return {
            "success": True,
            "message": "Documento eliminado correctamente.",
            "data": existing_document
        }

    except Exception as e:
        raise Exception(f"Error al eliminar datos: {str(e)}")


def get_dni(collection, dni):
    datos = read_data(collection)
    for persona in datos:
        if persona["DNI"] == dni:
            return True
    return False
