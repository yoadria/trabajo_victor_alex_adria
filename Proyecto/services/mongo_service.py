from pymongo import MongoClient
'''fichero que establece la conexion con la base de datos'''

class MongoService:
    
    def __init__(self, uri="mongodb://localhost:27017", db_name="ProyectoDB"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]
